<?php
// Efy claim intake: validate, relay to the authorized mailbox, acknowledge acceptance.
declare(strict_types=1);
ini_set('display_errors', '0');
date_default_timezone_set('America/Guayaquil');
const RECIPIENT = 'siniestros@efyseguros.com';
const VERSION = 'claims-20261009';
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, max-age=0');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');

function respond(int $status, array $data): void {
    http_response_code($status);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
function bytes(string $value): int {
    $last = strtolower(substr(trim($value), -1));
    $number = (int)$value;
    return $number * ($last === 'g' ? 1073741824 : ($last === 'm' ? 1048576 : ($last === 'k' ? 1024 : 1)));
}
function limits(): array {
    $post = bytes((string)ini_get('post_max_size'));
    $upload = bytes((string)ini_get('upload_max_filesize'));
    $post = $post > 0 ? min($post, 8388608) : 8388608;
    return ['max_files' => 3, 'file_bytes' => min(2097152, $upload > 0 ? $upload : 2097152), 'total_bytes' => min(6291456, max(0, $post - 65536)), 'post_bytes' => $post];
}
function privateDirectory(): string {
    $path = getenv('EFY_CLAIMS_STATE_DIR') ?: dirname(__DIR__, 3) . '/.efy-siniestros';
    if (!is_dir($path) && !@mkdir($path, 0700, true)) throw new RuntimeException('state unavailable');
    $real = realpath($path);
    $public = realpath(dirname(__DIR__, 2));
    if (!$real || !$public || $real === $public || strpos($real, $public . DIRECTORY_SEPARATOR) === 0 || !is_writable($real)) throw new RuntimeException('private state unavailable');
    if (!@chmod($real, 0700)) throw new RuntimeException('state permissions unavailable');
    return $real;
}
function field(string $name, int $max, bool $required, array &$errors): string {
    $raw = $_POST[$name] ?? '';
    if (!is_string($raw) || strlen($raw) > $max * 4 || !preg_match('//u', $raw) || preg_match('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/', $raw)) {
        $errors[$name] = 'Revisa este dato.';
        return '';
    }
    $value = trim($raw);
    if (($required && $value === '') || preg_match_all('/./us', $value) > $max) $errors[$name] = 'Completa este dato sin superar ' . $max . ' caracteres.';
    return $value;
}
function saveRecord($handle, array $record): void {
    $json = json_encode($record, JSON_UNESCAPED_SLASHES);
    if ($json === false || !rewind($handle) || !ftruncate($handle, 0) || fwrite($handle, $json) !== strlen($json) || !fflush($handle)) throw new RuntimeException('state write failed');
}
function rateLimit(string $directory): bool {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $salt = $directory . '/salt';
    $handle = @fopen($salt, 'c+');
    if (!$handle || !flock($handle, LOCK_EX)) throw new RuntimeException('rate state unavailable');
    @chmod($salt, 0600);
    $secret = stream_get_contents($handle);
    if (!$secret) {
        $secret = bin2hex(random_bytes(32));
        if (fwrite($handle, $secret) !== strlen($secret) || !fflush($handle)) throw new RuntimeException('rate state write failed');
    }
    flock($handle, LOCK_UN);
    fclose($handle);
    $filename = $directory . '/rate-' . hash_hmac('sha256', $ip, $secret) . '.json';
    $handle = @fopen($filename, 'c+');
    if (!$handle || !flock($handle, LOCK_EX)) throw new RuntimeException('rate state unavailable');
    @chmod($filename, 0600);
    $record = json_decode(stream_get_contents($handle), true) ?: [];
    $recent = array_values(array_filter($record['attempts'] ?? [], function ($time) { return is_int($time) && $time > time() - 3600; }));
    $allowed = count($recent) < 10;
    if ($allowed) $recent[] = time();
    saveRecord($handle, ['attempts' => $recent]);
    flock($handle, LOCK_UN);
    fclose($handle);
    return $allowed;
}

try {
    $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
    if (!in_array($method, ['GET', 'POST'], true)) { header('Allow: GET, POST'); respond(405, ['ok' => false, 'message' => 'Método no permitido.']); }
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    if ($origin !== '') {
        $host = strtolower((string)parse_url($origin, PHP_URL_HOST));
        $scheme = parse_url($origin, PHP_URL_SCHEME);
        $local = PHP_SAPI === 'cli-server' && in_array($host, ['localhost', '127.0.0.1'], true);
        if (!$local && ($scheme !== 'https' || !in_array($host, ['www.efyseguros.com', 'efyseguros.com'], true))) respond(403, ['ok' => false, 'message' => 'Abre el formulario desde la web de Efy.']);
    }
    $secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || ($_SERVER['SERVER_PORT'] ?? '') === '443';
    session_name('EFYCLAIMS');
    session_set_cookie_params(['lifetime' => 0, 'path' => '/nueva/', 'secure' => $secure, 'httponly' => true, 'samesite' => 'Lax']);
    if (!session_start()) throw new RuntimeException('session unavailable');
    if (empty($_SESSION['claims_csrf'])) $_SESSION['claims_csrf'] = bin2hex(random_bytes(32));
    $csrf = $_SESSION['claims_csrf'];
    session_write_close();
    $directory = privateDirectory();
    $bounds = limits();
    $ready = function_exists('mail') && function_exists('finfo_open') && $bounds['file_bytes'] > 0 && $bounds['total_bytes'] > 0;
    if ($method === 'GET') respond(200, ['ok' => true, 'version' => VERSION, 'ready' => $ready, 'recipient' => RECIPIENT, 'csrf' => $csrf, 'limits' => $bounds]);
    if (!$ready) respond(503, ['ok' => false, 'message' => 'El envío no está disponible. Puedes escribir a ' . RECIPIENT . '.']);
    if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > $bounds['post_bytes']) respond(413, ['ok' => false, 'message' => 'Los archivos superan el tamaño total permitido. Reduce los adjuntos e inténtalo de nuevo.']);
    if (!is_string($_POST['csrf'] ?? null) || !hash_equals($csrf, $_POST['csrf'])) respond(419, ['ok' => false, 'message' => 'La sesión del formulario venció. Vuelve a intentarlo.']);
    if (!empty($_POST['website'])) respond(422, ['ok' => false, 'message' => 'Revisa los datos del formulario.']);
    $requestId = $_POST['request_id'] ?? '';
    if (!is_string($requestId) || !preg_match('/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i', $requestId)) respond(422, ['ok' => false, 'message' => 'Actualiza el formulario y vuelve a intentarlo.']);

    $errors = [];
    $data = [];
    foreach (['name'=>[120,true], 'phone'=>[25,true], 'email'=>[254,false], 'insurer'=>[100,false], 'policy'=>[100,false], 'event_type'=>[20,true], 'event_date'=>[10,true], 'event_time'=>[5,false], 'location'=>[240,true], 'description'=>[4000,true]] as $key => $rule) $data[$key] = field($key, $rule[0], $rule[1], $errors);
    if (strlen($data['name']) < 2) $errors['name'] = 'Escribe tu nombre.';
    $digits = preg_replace('/\D/', '', $data['phone']);
    if (!preg_match('/^\+?[0-9 ()-]+$/', $data['phone']) || strlen($digits) < 7 || strlen($digits) > 15) $errors['phone'] = 'Escribe un teléfono válido, con código de país si corresponde.';
    if ($data['email'] !== '' && !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) $errors['email'] = 'Revisa el correo electrónico.';
    if (!in_array($data['event_type'], ['Accidente', 'Daños', 'Robo', 'Otro evento'], true)) $errors['event_type'] = 'Selecciona el tipo de evento.';
    $date = DateTimeImmutable::createFromFormat('!Y-m-d', $data['event_date']);
    if (!$date || $date->format('Y-m-d') !== $data['event_date'] || $data['event_date'] > date('Y-m-d')) $errors['event_date'] = 'Selecciona una fecha válida, que no esté en el futuro.';
    if ($data['event_time'] !== '' && !preg_match('/^(?:[01][0-9]|2[0-3]):[0-5][0-9]$/', $data['event_time'])) $errors['event_time'] = 'Revisa la hora del evento.';
    if (preg_match_all('/./us', $data['description']) < 20) $errors['description'] = 'Describe lo ocurrido con al menos 20 caracteres.';
    if (($_POST['consent'] ?? '') !== '1') $errors['consent'] = 'Confirma la autorización para gestionar el reporte.';

    $attachments = [];
    $uploads = $_FILES['attachments'] ?? null;
    if ($uploads !== null) {
        if (!is_array($uploads) || !is_array($uploads['error'] ?? null) || count($uploads['error']) > $bounds['max_files']) $errors['attachments'] = 'Adjunta como máximo tres archivos.';
        else {
            $total = 0;
            $detector = finfo_open(FILEINFO_MIME_TYPE);
            foreach ($uploads['error'] as $index => $error) {
                if ($error === UPLOAD_ERR_NO_FILE) continue;
                $temp = $uploads['tmp_name'][$index] ?? '';
                if ($error !== UPLOAD_ERR_OK || !is_string($temp) || !is_uploaded_file($temp)) { $errors['attachments'] = 'No se pudo cargar un adjunto. Revisa el archivo y su tamaño.'; break; }
                $size = filesize($temp);
                $mime = finfo_file($detector, $temp);
                $extensions = ['image/jpeg'=>'jpg', 'image/png'=>'png', 'image/webp'=>'webp', 'application/pdf'=>'pdf'];
                if ($size === false || $size < 1 || $size > $bounds['file_bytes'] || !isset($extensions[$mime])) { $errors['attachments'] = 'Usa fotos JPG, PNG o WebP, o documentos PDF, dentro del tamaño permitido.'; break; }
                $total += $size;
                if ($total > $bounds['total_bytes']) { $errors['attachments'] = 'Los adjuntos superan el tamaño total permitido.'; break; }
                $attachments[] = ['path'=>$temp, 'mime'=>$mime, 'name'=>'adjunto-' . (count($attachments)+1) . '.' . $extensions[$mime], 'hash'=>hash_file('sha256', $temp)];
            }
            finfo_close($detector);
        }
    }
    if ($errors) respond(422, ['ok'=>false, 'message'=>'Revisa los campos indicados antes de enviar.', 'errors'=>$errors]);
    $digest = hash('sha256', json_encode([$data, array_column($attachments, 'hash')], JSON_UNESCAPED_UNICODE));
    $filename = $directory . '/request-' . hash('sha256', $requestId) . '.json';
    $newRequest = !file_exists($filename);
    if ($newRequest && !rateLimit($directory)) { header('Retry-After: 3600'); respond(429, ['ok'=>false, 'message'=>'Has alcanzado el límite de envíos. Puedes escribir a ' . RECIPIENT . ' o volver a intentarlo más tarde.']); }
    $handle = @fopen($filename, 'c+');
    if (!$handle) throw new RuntimeException('request state unavailable');
    @chmod($filename, 0600);
    if (!flock($handle, LOCK_EX | LOCK_NB)) respond(409, ['ok'=>false, 'message'=>'El envío sigue en proceso. Espera antes de volver a intentarlo.']);
    $record = json_decode(stream_get_contents($handle), true) ?: [];
    if ($record && ($record['digest'] ?? '') !== $digest) respond(409, ['ok'=>false, 'message'=>'Este intento corresponde a otro reporte. Actualiza el formulario antes de enviar.']);
    if (($record['state'] ?? '') === 'accepted') respond(200, ['ok'=>true, 'reference'=>$record['reference'], 'received_at'=>$record['received_at'], 'recipient'=>RECIPIENT]);
    if (($record['state'] ?? '') === 'processing') respond(409, ['ok'=>false, 'reference'=>$record['reference'], 'message'=>'No podemos confirmar el resultado de este intento. No repitas el reporte; consulta a ' . RECIPIENT . ' indicando la referencia ' . $record['reference'] . '.']);
    if (!$newRequest && !rateLimit($directory)) { header('Retry-After: 3600'); respond(429, ['ok'=>false, 'message'=>'Has alcanzado el límite de envíos. Puedes escribir a ' . RECIPIENT . ' o volver a intentarlo más tarde.']); }
    $reference = $record['reference'] ?? 'EFY-' . date('Ymd') . '-' . strtoupper(bin2hex(random_bytes(5)));
    $record = ['digest'=>$digest, 'reference'=>$reference, 'state'=>'processing', 'updated_at'=>time()];
    saveRecord($handle, $record);

    $text = "NUEVO REPORTE DE SINIESTRO PARA EFY\nReferencia: $reference\nFecha de recepción: " . date('c') . "\n\nDATOS DE CONTACTO\nNombre: {$data['name']}\nTeléfono: {$data['phone']}\nCorreo: " . ($data['email'] ?: 'No indicado') . "\n\nEVENTO\nTipo: {$data['event_type']}\nFecha: {$data['event_date']}\nHora (Quito): " . ($data['event_time'] ?: 'No indicada') . "\nLugar: {$data['location']}\nAseguradora: " . ($data['insurer'] ?: 'No indicada') . "\nPóliza: " . ($data['policy'] ?: 'No indicada') . "\n\nDESCRIPCIÓN\n{$data['description']}\n\nAdjuntos: " . count($attachments) . "\nEl remitente autorizó usar estos datos para gestionar el reporte y contactarlo.\nOrigen: formulario de la web de Efy.\nEste aviso no confirma cobertura ni aceptación por la aseguradora.\n";
    $headers = ['From: Efy Seguros <' . RECIPIENT . '>', 'MIME-Version: 1.0', 'X-Efy-Reference: ' . $reference];
    if ($data['email'] !== '') $headers[] = 'Reply-To: ' . $data['email'];
    if ($attachments) {
        $boundary = 'efy_' . bin2hex(random_bytes(20));
        $headers[] = 'Content-Type: multipart/mixed; boundary="' . $boundary . '"';
        $message = '--' . $boundary . "\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($text));
        foreach ($attachments as $file) $message .= '--' . $boundary . "\r\nContent-Type: " . $file['mime'] . '; name="' . $file['name'] . '"' . "\r\nContent-Disposition: attachment; filename=\"" . $file['name'] . "\"\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode(file_get_contents($file['path'])));
        $message .= '--' . $boundary . "--\r\n";
    } else {
        $headers[] = 'Content-Type: text/plain; charset=UTF-8';
        $headers[] = 'Content-Transfer-Encoding: base64';
        $message = chunk_split(base64_encode($text));
    }
    $subject = '=?UTF-8?B?' . base64_encode('Reporte de siniestro · ' . $reference) . '?=';
    $accepted = @mail(RECIPIENT, $subject, $message, implode("\r\n", $headers), '-f' . RECIPIENT);
    if (!$accepted) {
        $record['state'] = 'failed';
        saveRecord($handle, $record);
        respond(503, ['ok'=>false, 'message'=>'No se pudo completar el envío. Conserva los datos e inténtalo de nuevo, o escribe a ' . RECIPIENT . '.']);
    }
    $record['state'] = 'accepted';
    $record['received_at'] = date('c');
    saveRecord($handle, $record);
    flock($handle, LOCK_UN);
    fclose($handle);
    // Keep only short-lived hashes/references for retry protection; no report data or attachments are stored here.
    foreach (glob($directory . '/*.json') ?: [] as $old) if (filemtime($old) < time() - 604800) @unlink($old);
    respond(200, ['ok'=>true, 'reference'=>$reference, 'received_at'=>$record['received_at'], 'recipient'=>RECIPIENT]);
} catch (Throwable $error) {
    respond(503, ['ok'=>false, 'message'=>'El envío no está disponible en este momento. Conserva tu información y escribe a ' . RECIPIENT . '.']);
}
