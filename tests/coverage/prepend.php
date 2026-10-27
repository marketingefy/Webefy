<?php
// Test-only transport. No upstream HTTP request can be issued by this harness.
declare(strict_types=1);
define('EFY_MASIVOS_LIBRARY_ONLY', true);
require '/site/public/nueva/api/coberturas.php';

$scenario = $_SERVER['HTTP_X_EFY_TEST_SCENARIO'] ?? 'match';
if ($scenario === 'unconfigured') putenv('EFY_MASIVOS_CONFIG_FILE=/fixtures/missing.php');
if ($scenario === 'public-config') putenv('EFY_MASIVOS_CONFIG_FILE=/site/public/nueva/api/coberturas.php');
if (in_array($scenario, ['bad-url', 'bad-key', 'noisy-config'], true)) putenv('EFY_MASIVOS_CONFIG_FILE=/fixtures/' . $scenario . '.php');
if ($scenario === 'rotated-key') putenv('EFY_MASIVOS_CONFIG_FILE=/fixtures/rotated-key.php');
if ($scenario === 'trusted-ip-a') $_SERVER['REMOTE_ADDR'] = '192.0.2.10';
if ($scenario === 'trusted-ip-b') $_SERVER['REMOTE_ADDR'] = '192.0.2.11';
if ($scenario === 'session-identity') unset($_SERVER['REMOTE_ADDR']);

coverageHandleRequest(static function (array $config, string $cedula, string $visitor) use ($scenario): array {
    file_put_contents('/fixtures/calls.jsonl', json_encode(['key' => $config['key'], 'cedula' => $cedula, 'visitor' => $visitor]) . "\n", FILE_APPEND);
    $failures = [
        'unauthorized' => [502, 'UPSTREAM_AUTHENTICATION'],
        'forbidden' => [502, 'UPSTREAM_ACCESS_DENIED'],
        'unavailable' => [502, 'UPSTREAM_UNAVAILABLE'],
        'http-error' => [502, 'UPSTREAM_HTTP_ERROR'],
        'busy' => [429, 'UPSTREAM_RATE_LIMITED'],
        'timeout' => [504, 'UPSTREAM_TIMEOUT'],
        'tls' => [502, 'UPSTREAM_TLS_ERROR'],
        'connection' => [502, 'UPSTREAM_CONNECTION_ERROR'],
        'invalid-json' => [502, 'UPSTREAM_RESPONSE_INVALID'],
        'unsafe-reason' => [502, 'RAW_PRIVATE_ERROR_' . $config['key']],
    ];
    if (isset($failures[$scenario])) return ['status' => $failures[$scenario][0], 'reason' => $failures[$scenario][1], 'data' => ['private_body' => 'NOMBRE PRIVADO', 'key' => $config['key']]];
    if (strpos($scenario, 'retry-') === 0) {
        $retry = ['retry-min' => 1, 'retry-max' => 3600, 'retry-zero' => 0, 'retry-large' => 3601, 'retry-unsafe' => "60\r\nX-Evil: yes"][$scenario];
        return ['status' => 429, 'reason' => 'UPSTREAM_RATE_LIMITED', 'retry_after' => $retry, 'data' => null];
    }
    if ($scenario === 'internal-error') throw new RuntimeException('RAW_PRIVATE_ERROR_' . $config['key']);
    $record = [
        'id' => 'private-internal-id', 'cedula' => $cedula, 'nombre' => 'NOMBRE PRIVADO',
        'fecha_nacimiento' => '1980-01-01', 'genero' => 'PRIVADO', 'origen' => 'archivo-privado.csv',
        'aseguradora' => 'PROASSISLIFE', 'contrato' => 'PRUEBA-001',
        'vigencia_inicio' => '2026-01-01', 'vigencia_fin' => '2027-01-01', 'estado' => 'VIGENTE',
    ];
    $data = [
        'encontrado' => $scenario !== 'no-match', 'fecha_consulta' => '2026-10-26',
        'fuentes_consultadas' => ['PROASSISLIFE'], 'fuentes_pendientes' => ['PRIVILEGIO'],
        'advertencias' => ['NOMBRE PRIVADO: un texto que no debe salir al navegador.'],
        'registros' => $scenario === 'no-match' ? [] : [$record],
    ];
    if ($scenario === 'multiple') {
        $record['contrato'] = 'PRUEBA-002';
        $record['estado'] = 'VENCIDA';
        $record['vigencia_inicio'] = null;
        $record['vigencia_fin'] = null;
        $data['registros'][] = $record;
    }
    if ($scenario === 'malformed') unset($data['registros'][0]['aseguradora']);
    if ($scenario === 'inconsistent') $data['encontrado'] = false;
    return ['status' => 200, 'data' => $data];
});
