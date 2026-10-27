"""Report bounded readiness flags without printing private configuration or SSH output."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.error
import urllib.request

from deploy_sftp import key_agent, required


ENDPOINT = 'https://www.efyseguros.com/nueva/api/coberturas.php'
REMOTE_FLAGS = (
    'config_file_exists', 'config_file_readable', 'returns_array',
    'has_unexpected_output', 'key_format_valid', 'analyzer_url_valid',
    'cli_curl_available', 'endpoint_helpers_available',
    'endpoint_config_valid', 'endpoint_state_directory_writable',
)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file, code, message, headers, new_url):
        return None

# No configuration content is echoed. Both PHP and Python suppress untrusted output.
REMOTE_PHP = r'''<?php
ini_set('display_errors', '0');
ini_set('log_errors', '0');
error_reporting(0);
$flags = [
    'config_file_exists' => false, 'config_file_readable' => false,
    'returns_array' => false, 'has_unexpected_output' => false,
    'key_format_valid' => false, 'analyzer_url_valid' => false,
    'cli_curl_available' => function_exists('curl_init'),
    'endpoint_helpers_available' => false, 'endpoint_config_valid' => false,
    'endpoint_state_directory_writable' => false,
];
$file = '/home1/brayanez/efy-secrets/masivos.php';
$flags['config_file_exists'] = is_file($file);
$flags['config_file_readable'] = is_readable($file);
$initialLevel = ob_get_level();
ob_start();
try {
    if ($flags['config_file_exists'] && $flags['config_file_readable']) {
        $config = (static function ($path) { return require $path; })($file);
        $flags['returns_array'] = is_array($config);
        if (is_array($config)) {
            $key = $config['MASIVOS_API_KEY'] ?? null;
            $url = $config['EFYANALYZER_URL'] ?? null;
            $flags['key_format_valid'] = is_string($key) && preg_match('/^[A-Za-z0-9_-]{32,256}$/D', $key) === 1;
            $flags['analyzer_url_valid'] = is_string($url) && rtrim($url, '/') === 'https://app.latamyanez.com';
        }
    }
} catch (Throwable $error) { /* Only the flags leave this process. */ }
while (ob_get_level() > $initialLevel) {
    if (ob_get_clean() !== '') $flags['has_unexpected_output'] = true;
}
$initialLevel = ob_get_level();
ob_start();
try {
    define('EFY_MASIVOS_LIBRARY_ONLY', true);
    $_SERVER['DOCUMENT_ROOT'] = '/home1/brayanez/public_html';
    require '/home1/brayanez/public_html/nueva/api/coberturas.php';
    $flags['endpoint_helpers_available'] = function_exists('coverageConfiguration') && function_exists('coveragePrivateDirectory');
    if ($flags['endpoint_helpers_available']) {
        $flags['endpoint_config_valid'] = coverageConfiguration() !== null;
        try {
            $directory = coveragePrivateDirectory();
            $flags['endpoint_state_directory_writable'] = is_dir($directory) && is_writable($directory);
        } catch (Throwable $error) { /* No paths or exception messages are exposed. */ }
    }
} catch (Throwable $error) { /* No paths or exception messages are exposed. */ }
while (ob_get_level() > $initialLevel) {
    if (ob_get_clean() !== '') $flags['has_unexpected_output'] = true;
}
echo json_encode($flags);
'''


def endpoint_flags():
    flags = {
        'endpoint_http_status': 0, 'endpoint_ok': False, 'endpoint_ready': False,
        'endpoint_expected_version': False, 'endpoint_csrf_valid': False,
    }
    try:
        request = urllib.request.Request(ENDPOINT, headers={'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0'})
        try:
            response = urllib.request.build_opener(NoRedirect()).open(request, timeout=15)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            flags['endpoint_http_status'] = response.status
            body = response.read(8193)
        if len(body) > 8192:
            return flags
        data = json.loads(body)
        if not isinstance(data, dict):
            return flags
        flags['endpoint_ok'] = data.get('ok') is True
        flags['endpoint_ready'] = data.get('ready') is True
        flags['endpoint_expected_version'] = data.get('version') == 'coverage-20261026'
        csrf = data.get('csrf')
        flags['endpoint_csrf_valid'] = isinstance(csrf, str) and re.fullmatch(r'[a-f0-9]{64}', csrf) is not None
    except Exception:
        # HTTP bodies, request identifiers, redirects and exception strings stay private.
        pass
    return flags


def safe_remote_flags(output):
    """Reconstruct the allowlist; never relay a remote JSON value verbatim."""
    if len(output) > 8192:
        raise ValueError('Invalid diagnostic response')
    data = json.loads(output)
    if not isinstance(data, dict) or any(type(data.get(key)) is not bool for key in REMOTE_FLAGS):
        raise ValueError('Invalid diagnostic response')
    return {key: data[key] for key in REMOTE_FLAGS}


def remote_flags():
    host = required('SSH_HOST')
    user = required('SSH_USER')
    key = required('SSH_PRIVATE_KEY')
    port = int(os.environ.get('SSH_PORT', '2222'))
    if not re.fullmatch(r'[A-Za-z0-9.-]+', host) or not re.fullmatch(r'[A-Za-z0-9_-]+', user) or not 1 <= port <= 65535:
        raise ValueError('Invalid SSH settings')
    known_hosts = os.environ.get('SSH_KNOWN_HOSTS', '').strip()
    if not known_hosts:
        known_hosts = (Path(__file__).resolve().parents[1] / '.github/hostgator_known_hosts').read_text()
    with tempfile.TemporaryDirectory(prefix='efy-masivos-check-') as temporary:
        root = Path(temporary)
        root.chmod(0o700)
        key_path = root / 'key'
        key_path.write_text(key + '\n')
        key_path.chmod(0o600)
        hosts_path = root / 'known_hosts'
        hosts_path.write_text(known_hosts + '\n')
        hosts_path.chmod(0o600)
        with key_agent(root, key_path, os.environ.get('SSH_KEY_PASSPHRASE', '')) as agent_env:
            result = subprocess.run(
                ['ssh', '-i', str(key_path), '-p', str(port),
                 '-o', 'BatchMode=yes', '-o', 'IdentitiesOnly=yes',
                 '-o', 'StrictHostKeyChecking=yes', '-o', 'ConnectTimeout=20',
                 '-o', 'UserKnownHostsFile=' + str(hosts_path), user + '@' + host,
                 'php -d display_errors=0 -d log_errors=0'],
                input=REMOTE_PHP, capture_output=True, text=True, timeout=40, env=agent_env,
            )
        if result.returncode:
            raise ValueError('Remote diagnostic unavailable')
        return safe_remote_flags(result.stdout)


def main():
    flags = endpoint_flags()
    flags['ssh_diagnostic_completed'] = False
    try:
        flags.update(remote_flags())
        flags['ssh_diagnostic_completed'] = True
    except Exception:
        # Never print stderr, stdout, credentials or exception details.
        pass
    print(json.dumps(flags, sort_keys=True))
    return 0 if flags['ssh_diagnostic_completed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
