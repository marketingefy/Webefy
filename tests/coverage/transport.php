<?php
// Invoke with the five cURL functions below disabled so PHP permits these stubs.
declare(strict_types=1);
define('EFY_MASIVOS_LIBRARY_ONLY', true);
require '/site/public/nueva/api/coberturas.php';

$GLOBALS['scenario'] = 'match';
function curl_init($url) { $GLOBALS['url'] = $url; return (object)[]; }
function curl_setopt_array($curl, $options) { $GLOBALS['options'] = $options; return true; }
function curl_exec($curl) {
    if ($GLOBALS['scenario'] === 'timeout') return false;
    $body = $GLOBALS['scenario'] === 'malformed' ? '{invalid' : json_encode(['encontrado' => false]);
    if ($GLOBALS['scenario'] === 'oversized') $body = str_repeat('x', 262145);
    return ($GLOBALS['options'][CURLOPT_WRITEFUNCTION])($curl, $body) === strlen($body);
}
function curl_getinfo($curl, $option) { return $GLOBALS['scenario'] === 'unauthorized' ? 401 : ($GLOBALS['scenario'] === 'busy' ? 429 : 200); }
function curl_errno($curl) { return $GLOBALS['scenario'] === 'timeout' ? CURLE_OPERATION_TIMEDOUT : 0; }
function curl_close($curl) {}
function check($condition, $message) { if (!$condition) throw new RuntimeException($message); }

$key = str_repeat('x', 48);
coverageRequest(['key' => $key], '0000000001');
$options = $GLOBALS['options'];
check($GLOBALS['url'] === COVERAGE_API_URL && strpos($GLOBALS['url'], '?') === false, 'Fixed endpoint without query');
check(json_decode($options[CURLOPT_POSTFIELDS], true) === ['cedula' => '0000000001'], 'String identifier preserves zeroes');
check(in_array('Authorization: Bearer ' . $key, $options[CURLOPT_HTTPHEADER], true), 'Server bearer credential');
check(in_array('Content-Type: application/json', $options[CURLOPT_HTTPHEADER], true), 'JSON request');
check($options[CURLOPT_SSL_VERIFYPEER] === true && $options[CURLOPT_SSL_VERIFYHOST] === 2, 'TLS verification');
check($options[CURLOPT_PROTOCOLS] === CURLPROTO_HTTPS && $options[CURLOPT_FOLLOWLOCATION] === false && $options[CURLOPT_MAXREDIRS] === 0, 'HTTPS without credential redirects');
check($options[CURLOPT_CONNECTTIMEOUT] > 0 && $options[CURLOPT_TIMEOUT] <= 15, 'Bounded request time');
foreach (['unauthorized' => 502, 'busy' => 429, 'timeout' => 504] as $scenario => $status) {
    $GLOBALS['scenario'] = $scenario;
    check(coverageRequest(['key' => $key], '0000000001')['status'] === $status, 'Transport error ' . $scenario);
}
$GLOBALS['scenario'] = 'malformed';
try { coverageRequest(['key' => $key], '0000000001'); throw new LogicException('Malformed JSON was accepted'); }
catch (JsonException $expected) {}
$GLOBALS['scenario'] = 'oversized';
$curl = curl_init(COVERAGE_API_URL);
// The callback must reject the whole chunk instead of accumulating unbounded data.
check(($GLOBALS['options'][CURLOPT_WRITEFUNCTION])($curl, str_repeat('x', 262145)) === 0, 'Bounded response size');
echo "PASS fixed HTTPS request, credential boundary, identifier, transport errors, response bounds\n";
