<?php
// Invoke with the six cURL functions below disabled so PHP permits these stubs.
declare(strict_types=1);
define('EFY_MASIVOS_LIBRARY_ONLY', true);
require '/site/public/nueva/api/coberturas.php';
ini_set('display_errors', '1'); // Only this isolated fake transport uses diagnostic output.

$GLOBALS['scenario'] = 'match';
function curl_init($url) { $GLOBALS['url'] = $url; return $GLOBALS['scenario'] === 'init-failed' ? false : (object)[]; }
function curl_setopt_array($curl, $options) { $GLOBALS['options'] = $options; return $GLOBALS['scenario'] !== 'options-failed'; }
function curl_exec($curl) {
    if (in_array($GLOBALS['scenario'], ['timeout', 'tls', 'connection', 'dns'], true)) return false;
    if ($GLOBALS['scenario'] === 'internal-error') throw new RuntimeException('RAW_PRIVATE_ERROR_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');
    $headers = $GLOBALS['options'][CURLOPT_HEADERFUNCTION];
    $headers($curl, "HTTP/1.1 429 Too Many Requests\r\n");
    $retryHeaders = ['retry-min' => "1", 'retry-max' => "3600", 'retry-zero' => "0", 'retry-large' => "3601",
        'retry-unsafe' => "60\r\nX-Evil: yes", 'retry-date' => 'Wed, 21 Oct 2026 07:28:00 GMT'];
    if (isset($retryHeaders[$GLOBALS['scenario']])) $headers($curl, 'Retry-After: ' . $retryHeaders[$GLOBALS['scenario']] . "\r\n");
    if ($GLOBALS['scenario'] === 'retry-block-reset') {
        $headers($curl, "Retry-After: 5\r\n");
        $headers($curl, "HTTP/1.1 429 Too Many Requests\r\n");
    }
    $body = $GLOBALS['scenario'] === 'malformed' ? '{RAW_PRIVATE_ERROR_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' : json_encode(['encontrado' => false]);
    if ($GLOBALS['scenario'] === 'oversized') $body = str_repeat('x', 262145);
    return ($GLOBALS['options'][CURLOPT_WRITEFUNCTION])($curl, $body) === strlen($body);
}
function curl_getinfo($curl, $option) {
    if (strpos($GLOBALS['scenario'], 'retry-') === 0) return 429;
    return ['unauthorized' => 401, 'forbidden' => 403, 'unavailable' => 503, 'http-error' => 500, 'busy' => 429][$GLOBALS['scenario']] ?? 200;
}
function curl_errno($curl) { return ['timeout' => CURLE_OPERATION_TIMEDOUT, 'tls' => 60, 'connection' => CURLE_COULDNT_CONNECT, 'dns' => CURLE_COULDNT_RESOLVE_HOST, 'oversized' => CURLE_WRITE_ERROR][$GLOBALS['scenario']] ?? 0; }
function curl_close($curl) {}
function check($condition, $message) { if (!$condition) throw new RuntimeException($message); }

$key = str_repeat('x', 48);
$visitor = str_repeat('a', 64);
check(coverageRequest(['key' => $key], '0000000001')['reason'] === 'PROXY_UNAVAILABLE', 'Missing visitor never reaches API');
check(coverageRequest(['key' => $key], '0000000001', "bad\r\nX-Evil: yes")['reason'] === 'PROXY_UNAVAILABLE', 'Invalid visitor never becomes a header');
coverageRequest(['key' => $key], '0000000001', $visitor);
$options = $GLOBALS['options'];
check($GLOBALS['url'] === COVERAGE_API_URL && strpos($GLOBALS['url'], '?') === false, 'Fixed endpoint without query');
check(json_decode($options[CURLOPT_POSTFIELDS], true) === ['cedula' => '0000000001'], 'String identifier preserves zeroes');
check(in_array('Authorization: Bearer ' . $key, $options[CURLOPT_HTTPHEADER], true), 'Server bearer credential');
check(in_array('X-Efy-Visitante: ' . $visitor, $options[CURLOPT_HTTPHEADER], true), 'Private visitor fingerprint header');
check(count(array_filter($options[CURLOPT_HTTPHEADER], static fn($header) => strpos($header, 'X-Efy-Visitante:') === 0)) === 1, 'Exactly one visitor header');
check(in_array('Content-Type: application/json', $options[CURLOPT_HTTPHEADER], true), 'JSON request');
check($options[CURLOPT_SSL_VERIFYPEER] === true && $options[CURLOPT_SSL_VERIFYHOST] === 2, 'TLS verification');
check($options[CURLOPT_PROTOCOLS] === CURLPROTO_HTTPS && $options[CURLOPT_FOLLOWLOCATION] === false && $options[CURLOPT_MAXREDIRS] === 0, 'HTTPS without credential redirects');
check($options[CURLOPT_CONNECTTIMEOUT] > 0 && $options[CURLOPT_TIMEOUT] <= 15, 'Bounded request time');
foreach ([
    'unauthorized' => [502, 'UPSTREAM_AUTHENTICATION'], 'forbidden' => [502, 'UPSTREAM_ACCESS_DENIED'],
    'unavailable' => [502, 'UPSTREAM_UNAVAILABLE'], 'http-error' => [502, 'UPSTREAM_HTTP_ERROR'],
    'busy' => [429, 'UPSTREAM_RATE_LIMITED'], 'timeout' => [504, 'UPSTREAM_TIMEOUT'],
    'tls' => [502, 'UPSTREAM_TLS_ERROR'], 'connection' => [502, 'UPSTREAM_CONNECTION_ERROR'],
    'dns' => [502, 'UPSTREAM_CONNECTION_ERROR'], 'malformed' => [502, 'UPSTREAM_RESPONSE_INVALID'],
    'oversized' => [502, 'UPSTREAM_RESPONSE_INVALID'], 'init-failed' => [502, 'PROXY_UNAVAILABLE'],
    'options-failed' => [502, 'PROXY_UNAVAILABLE'], 'internal-error' => [502, 'PROXY_UNAVAILABLE'],
] as $scenario => $expected) {
    $GLOBALS['scenario'] = $scenario;
    $result = coverageRequest(['key' => $key], '0000000001', $visitor);
    $failure = ['status' => $expected[0], 'data' => null, 'reason' => $expected[1]];
    if ($expected[0] === 429) $failure['retry_after'] = 60;
    check($result === $failure, 'Transport error ' . $scenario);
    check(strpos(json_encode($result), $key) === false && strpos(json_encode($result), 'RAW_PRIVATE_ERROR') === false, 'Private transport details excluded');
}
foreach (['retry-min' => 1, 'retry-max' => 3600, 'retry-zero' => 60, 'retry-large' => 60, 'retry-unsafe' => 60, 'retry-date' => 60, 'retry-block-reset' => 60] as $scenario => $seconds) {
    $GLOBALS['scenario'] = $scenario;
    $result = coverageRequest(['key' => $key], '0000000001', $visitor);
    check($result === ['status' => 429, 'data' => null, 'reason' => 'UPSTREAM_RATE_LIMITED', 'retry_after' => $seconds], 'Bounded retry header ' . $scenario);
}
echo "PASS fixed HTTPS request, credential boundary, identifier, transport errors, response bounds\n";
