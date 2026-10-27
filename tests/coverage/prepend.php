<?php
// Test-only transport. No upstream HTTP request can be issued by this harness.
declare(strict_types=1);
define('EFY_MASIVOS_LIBRARY_ONLY', true);
require '/site/public/nueva/api/coberturas.php';

$scenario = $_SERVER['HTTP_X_EFY_TEST_SCENARIO'] ?? 'match';
if ($scenario === 'unconfigured') putenv('EFY_MASIVOS_CONFIG_FILE=/fixtures/missing.php');
if ($scenario === 'public-config') putenv('EFY_MASIVOS_CONFIG_FILE=/site/public/nueva/api/coberturas.php');
if (in_array($scenario, ['bad-url', 'bad-key', 'noisy-config'], true)) putenv('EFY_MASIVOS_CONFIG_FILE=/fixtures/' . $scenario . '.php');

coverageHandleRequest(static function (array $config, string $cedula) use ($scenario): array {
    file_put_contents('/fixtures/calls.jsonl', json_encode(['key' => $config['key'], 'cedula' => $cedula]) . "\n", FILE_APPEND);
    if (in_array($scenario, ['unauthorized', 'unavailable', 'busy', 'timeout'], true)) {
        return ['status' => ['unauthorized' => 401, 'unavailable' => 503, 'busy' => 429, 'timeout' => 504][$scenario], 'data' => null];
    }
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
