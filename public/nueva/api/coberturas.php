<?php
// Coopartamos lookup. The API credential stays in private server configuration.
declare(strict_types=1);
ini_set('display_errors', '0');

const COVERAGE_API_URL = 'https://app.latamyanez.com/api/integraciones/masivos/coopartamos/consulta';
const COVERAGE_VERSION = 'coverage-20261026';
const COVERAGE_UNAVAILABLE = 'No pudimos consultar la cobertura en este momento. Inténtalo de nuevo o contacta al equipo de Efy.';

function coverageRespond(int $status, array $data): void {
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store, max-age=0');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: same-origin');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
}

function coveragePublicRoots(): array {
    $roots = [realpath(dirname(__DIR__, 2))];
    if (!empty($_SERVER['DOCUMENT_ROOT'])) $roots[] = realpath($_SERVER['DOCUMENT_ROOT']);
    return array_values(array_filter($roots));
}

function coverageIsPrivate(string $path): bool {
    foreach (coveragePublicRoots() as $root) {
        if ($path === $root || strpos($path, $root . DIRECTORY_SEPARATOR) === 0) return false;
    }
    return true;
}

function coverageConfiguration(): ?array {
    $path = realpath(getenv('EFY_MASIVOS_CONFIG_FILE') ?: '/home1/brayanez/efy-secrets/masivos.php');
    if (!$path || !coverageIsPrivate($path) || !is_file($path) || !is_readable($path)) return null;
    $level = ob_get_level();
    ob_start();
    try {
        $config = (static function (string $file) { return require $file; })($path);
        $output = ob_get_clean();
        if ($output !== '' || !is_array($config)) return null;
    } catch (Throwable $error) {
        while (ob_get_level() > $level) ob_end_clean();
        return null;
    }
    $key = $config['MASIVOS_API_KEY'] ?? null;
    $url = $config['EFYANALYZER_URL'] ?? null;
    if (!is_string($key) || !preg_match('/^[A-Za-z0-9_-]{32,256}$/D', $key)) return null;
    if (!is_string($url) || rtrim($url, '/') !== 'https://app.latamyanez.com') return null;
    return ['key' => $key];
}

function coveragePrivateDirectory(): string {
    $path = getenv('EFY_MASIVOS_STATE_DIR') ?: dirname(__DIR__, 3) . '/.efy-masivos';
    // Check the existing parent before creating a directory in a public location.
    $parent = realpath(dirname($path));
    if (!$parent || !coverageIsPrivate($parent)) throw new RuntimeException('private state unavailable');
    if (!is_dir($path) && !@mkdir($path, 0700)) throw new RuntimeException('state unavailable');
    $real = realpath($path);
    if (!$real || !coverageIsPrivate($real) || !is_writable($real) || !@chmod($real, 0700)) throw new RuntimeException('private state unavailable');
    return $real;
}

function coverageRateLimit(string $directory): bool {
    $saltPath = $directory . '/salt';
    $handle = @fopen($saltPath, 'c+');
    if (!$handle) throw new RuntimeException('rate state unavailable');
    try {
        if (!@chmod($saltPath, 0600) || !flock($handle, LOCK_EX)) throw new RuntimeException('rate state unavailable');
        $salt = stream_get_contents($handle);
        if ($salt === '') {
            $salt = bin2hex(random_bytes(32));
            if (fwrite($handle, $salt) !== strlen($salt) || !fflush($handle)) throw new RuntimeException('rate state unavailable');
        }
    } finally { fclose($handle); }
    $ip = (string)($_SERVER['REMOTE_ADDR'] ?? 'unknown');
    $path = $directory . '/rate-' . hash_hmac('sha256', $ip, $salt) . '.json';
    $handle = @fopen($path, 'c+');
    if (!$handle) throw new RuntimeException('rate state unavailable');
    try {
        if (!@chmod($path, 0600) || !flock($handle, LOCK_EX)) throw new RuntimeException('rate state unavailable');
        $record = json_decode(stream_get_contents($handle), true);
        $recent = is_array($record) ? array_values(array_filter($record, static function ($time) { return is_int($time) && $time > time() - 900; })) : [];
        $allowed = count($recent) < 10;
        if ($allowed) $recent[] = time();
        $json = json_encode($recent);
        if (!rewind($handle) || !ftruncate($handle, 0) || fwrite($handle, $json) !== strlen($json) || !fflush($handle)) throw new RuntimeException('rate state unavailable');
        return $allowed;
    } finally { fclose($handle); }
}

function coverageOriginAllowed(): bool {
    if (($_SERVER['HTTP_SEC_FETCH_SITE'] ?? '') === 'cross-site') return false;
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    if ($origin === '') return true; // CSRF validation remains mandatory for POST.
    $parts = parse_url($origin);
    if (!is_array($parts) || isset($parts['user']) || isset($parts['pass']) || isset($parts['query']) || isset($parts['fragment']) || !empty($parts['path'])) return false;
    $host = strtolower($parts['host'] ?? '');
    if (PHP_SAPI === 'cli-server' && in_array($host, ['127.0.0.1', 'localhost'], true)) {
        return ($parts['scheme'] ?? '') === 'http' && (string)($parts['port'] ?? 80) === (string)($_SERVER['SERVER_PORT'] ?? 80);
    }
    return ($parts['scheme'] ?? '') === 'https' && (!isset($parts['port']) || $parts['port'] === 443) && in_array($host, ['www.efyseguros.com', 'efyseguros.com'], true);
}

function coverageText($value, int $max): string {
    if (!is_string($value) || strlen($value) > $max * 4 || !preg_match('//u', $value) || preg_match('/[\x00-\x1F\x7F]/', $value) || preg_match_all('/./us', $value) > $max) throw new RuntimeException('invalid upstream response');
    return trim($value);
}

function coverageDate($value): ?string {
    if ($value === null) return null;
    if (!is_string($value)) throw new RuntimeException('invalid upstream date');
    $date = DateTimeImmutable::createFromFormat('!Y-m-d', $value);
    if (!$date || $date->format('Y-m-d') !== $value) throw new RuntimeException('invalid upstream date');
    return $value;
}

function coveragePublicResult(array $data): array {
    if (!is_bool($data['encontrado'] ?? null) || !is_array($data['registros'] ?? null) || array_values($data['registros']) !== $data['registros'] || count($data['registros']) > 100) throw new RuntimeException('invalid upstream response');
    $records = [];
    foreach ($data['registros'] as $record) {
        if (!is_array($record)) throw new RuntimeException('invalid upstream record');
        $insurer = $record['aseguradora'] ?? null;
        $state = $record['estado'] ?? null;
        if (!in_array($insurer, ['PROASSISLIFE', 'PRIVILEGIO'], true) || !in_array($state, ['VIGENTE', 'POR_INICIAR', 'VENCIDA', 'NO_DETERMINADA'], true)) throw new RuntimeException('invalid upstream record');
        $records[] = [
            'aseguradora' => $insurer,
            'contrato' => coverageText($record['contrato'] ?? null, 160),
            'vigencia_inicio' => coverageDate($record['vigencia_inicio'] ?? null),
            'vigencia_fin' => coverageDate($record['vigencia_fin'] ?? null),
            'estado' => $state,
        ];
    }
    if ($data['encontrado'] !== (count($records) > 0)) throw new RuntimeException('inconsistent upstream response');
    $consulted = coverageDate($data['fecha_consulta'] ?? null);
    if ($consulted === null) throw new RuntimeException('invalid upstream date');
    // Only documented portfolio identifiers cross the public boundary.
    $pending = $data['fuentes_pendientes'] ?? null;
    if (!is_array($pending) || array_values($pending) !== $pending) throw new RuntimeException('invalid upstream sources');
    foreach ($pending as $source) if (!in_array($source, ['PRIVILEGIO', 'PROASSISLIFE'], true)) throw new RuntimeException('invalid upstream source');
    $pending = array_values(array_unique($pending));
    // Upstream free text is not relayed: it could contain personal information.
    $warnings = ['La vigencia corresponde al listado recibido; no acredita pagos ni cancelaciones posteriores.'];
    if (in_array('PRIVILEGIO', $pending, true)) $warnings[] = 'La cartera de Privilegio está pendiente de incorporación. Esta consulta no permite descartar una cobertura con esa aseguradora.';
    return ['ok' => true, 'encontrado' => $data['encontrado'], 'fecha_consulta' => $consulted, 'fuentes_pendientes' => $pending, 'registros' => $records, 'advertencias' => $warnings];
}

function coverageRequest(array $config, string $cedula): array {
    $curl = curl_init(COVERAGE_API_URL);
    if ($curl === false) throw new RuntimeException('upstream unavailable');
    $body = '';
    curl_setopt_array($curl, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode(['cedula' => $cedula]),
        CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . $config['key'], 'Content-Type: application/json', 'Accept: application/json'],
        CURLOPT_CONNECTTIMEOUT => 5,
        CURLOPT_TIMEOUT => 8,
        CURLOPT_FOLLOWLOCATION => false,
        CURLOPT_MAXREDIRS => 0,
        CURLOPT_PROTOCOLS => CURLPROTO_HTTPS,
        CURLOPT_SSL_VERIFYPEER => true,
        CURLOPT_SSL_VERIFYHOST => 2,
        CURLOPT_WRITEFUNCTION => static function ($handle, string $chunk) use (&$body): int {
            if (strlen($body) + strlen($chunk) > 262144) return 0;
            $body .= $chunk;
            return strlen($chunk);
        },
    ]);
    try {
        $success = curl_exec($curl);
        $status = (int)curl_getinfo($curl, CURLINFO_RESPONSE_CODE);
        $timeout = curl_errno($curl) === CURLE_OPERATION_TIMEDOUT;
        if ($success === false) return ['status' => $timeout ? 504 : 502, 'data' => null];
        if ($status !== 200) return ['status' => $status === 429 ? 429 : 502, 'data' => null];
        $data = json_decode($body, true, 32, JSON_THROW_ON_ERROR);
        if (!is_array($data)) throw new RuntimeException('invalid upstream response');
        return ['status' => 200, 'data' => $data];
    } finally { curl_close($curl); }
}

function coverageHandleRequest(?callable $transport = null): void {
    try {
        $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
        if (!in_array($method, ['GET', 'POST'], true)) { header('Allow: GET, POST'); coverageRespond(405, ['ok' => false, 'message' => 'Método no permitido.']); return; }
        if (!coverageOriginAllowed()) { coverageRespond(403, ['ok' => false, 'message' => 'Abre la consulta desde la web de Efy.']); return; }
        $secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || ($_SERVER['SERVER_PORT'] ?? '') === '443';
        session_name('EFYMASIVOS');
        session_set_cookie_params(['lifetime' => 0, 'path' => '/nueva/', 'secure' => $secure, 'httponly' => true, 'samesite' => 'Lax']);
        if (!session_start()) throw new RuntimeException('session unavailable');
        if (empty($_SESSION['masivos_csrf'])) $_SESSION['masivos_csrf'] = bin2hex(random_bytes(32));
        $csrf = $_SESSION['masivos_csrf'];
        session_write_close();
        $config = coverageConfiguration();
        $directory = null;
        try { $directory = coveragePrivateDirectory(); } catch (Throwable $error) { /* Availability is reported without private path details. */ }
        $ready = $config !== null && $directory !== null && (function_exists('curl_init') || $transport !== null);
        if ($method === 'GET') { coverageRespond(200, ['ok' => true, 'version' => COVERAGE_VERSION, 'ready' => $ready, 'csrf' => $csrf]); return; }
        if (!$ready) { coverageRespond(503, ['ok' => false, 'message' => COVERAGE_UNAVAILABLE]); return; }
        if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 2048) { coverageRespond(413, ['ok' => false, 'message' => 'La solicitud supera el tamaño permitido.']); return; }
        if (strtolower(trim(explode(';', $_SERVER['CONTENT_TYPE'] ?? '')[0])) !== 'application/json') { coverageRespond(415, ['ok' => false, 'message' => 'Actualiza la página y vuelve a intentarlo.']); return; }
        $raw = file_get_contents('php://input', false, null, 0, 2049);
        if ($raw === false || strlen($raw) > 2048) { coverageRespond(413, ['ok' => false, 'message' => 'La solicitud supera el tamaño permitido.']); return; }
        $data = json_decode($raw, true);
        if (!is_array($data)) { coverageRespond(400, ['ok' => false, 'message' => 'Revisa los datos de la consulta.']); return; }
        if (!is_string($data['csrf'] ?? null) || !hash_equals($csrf, $data['csrf'])) { coverageRespond(419, ['ok' => false, 'message' => 'La sesión de la consulta venció. Actualiza la página e inténtalo otra vez.']); return; }
        if (($data['cooperativa'] ?? '') !== 'coopartamos' || ($data['consent'] ?? null) !== true || !is_string($data['cedula'] ?? null) || !preg_match('/^[0-9]{10}$/D', $data['cedula'])) { coverageRespond(422, ['ok' => false, 'message' => 'Selecciona Coopartamos, escribe los 10 dígitos de tu cédula y confirma la autorización.']); return; }
        if (!coverageRateLimit($directory)) { header('Retry-After: 900'); coverageRespond(429, ['ok' => false, 'message' => 'Has alcanzado el límite de consultas. Espera unos minutos o contacta al equipo de Efy.']); return; }
        $result = ($transport ?? 'coverageRequest')($config, $data['cedula']);
        if (($result['status'] ?? 502) !== 200) {
            $status = in_array($result['status'] ?? null, [429, 504], true) ? $result['status'] : 502;
            if ($status === 429) header('Retry-After: 60');
            coverageRespond($status, ['ok' => false, 'message' => $status === 429 ? 'La consulta está temporalmente ocupada. Espera un minuto e inténtalo de nuevo.' : COVERAGE_UNAVAILABLE]);
            return;
        }
        coverageRespond(200, coveragePublicResult($result['data']));
    } catch (Throwable $error) {
        // Do not log response bodies, credentials, cédulas, or configuration paths.
        coverageRespond(502, ['ok' => false, 'message' => COVERAGE_UNAVAILABLE]);
    }
}

// Tests can load pure validation helpers and inject an isolated transport.
if (!defined('EFY_MASIVOS_LIBRARY_ONLY')) coverageHandleRequest();
