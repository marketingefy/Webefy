"""Isolated coverage checks. Starts only its own PHP container and fake transport.

Run: python3 tests/coverage/test_api.py
Requires Docker with php:8.3-cli. No real key, upstream request or customer data.
"""
import http.cookiejar
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
import unittest
import urllib.error
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[2]
DOCKER = ['docker', '--host=unix:///var/run/docker.sock']
KEY = 'x' * 48


def docker(*args):
    env = os.environ.copy()
    for name in ['DOCKER_HOST', 'DOCKER_CONTEXT', 'DOCKER_TLS', 'DOCKER_TLS_VERIFY', 'DOCKER_CERT_PATH']:
        env.pop(name, None)
    return subprocess.check_output(DOCKER + list(args), env=env, text=True, stderr=subprocess.STDOUT)


class CoverageApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = Path(tempfile.mkdtemp(prefix='efy-coverage-'))
        (cls.fixtures / 'masivos.php').write_text("<?php return ['MASIVOS_API_KEY'=>'" + KEY + "','EFYANALYZER_URL'=>'https://app.latamyanez.com'];\n")
        (cls.fixtures / 'bad-url.php').write_text("<?php return ['MASIVOS_API_KEY'=>'" + KEY + "','EFYANALYZER_URL'=>'https://example.invalid'];\n")
        (cls.fixtures / 'bad-key.php').write_text("<?php return ['MASIVOS_API_KEY'=>'short','EFYANALYZER_URL'=>'https://app.latamyanez.com'];\n")
        (cls.fixtures / 'noisy-config.php').write_text("<?php echo 'private-config-output'; return ['MASIVOS_API_KEY'=>'" + KEY + "','EFYANALYZER_URL'=>'https://app.latamyanez.com'];\n")
        cls.container = 'efy-coverage-test-' + uuid.uuid4().hex[:10]
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            cls.port = sock.getsockname()[1]
        try:
            docker('run', '-d', '--name', cls.container,
                   '-p', f'127.0.0.1:{cls.port}:8088',
                   '--mount', f'type=bind,src={ROOT},dst=/site,readonly',
                   '--mount', f'type=bind,src={cls.fixtures},dst=/fixtures',
                   '-e', 'EFY_MASIVOS_CONFIG_FILE=/fixtures/masivos.php',
                   '-e', 'EFY_MASIVOS_STATE_DIR=/fixtures/state',
                   'php:8.3-cli', 'php', '-d', 'auto_prepend_file=/site/tests/coverage/prepend.php',
                   '-S', '0.0.0.0:8088', '-t', '/site/public')
            cls.base = f'http://127.0.0.1:{cls.port}/nueva/api/coberturas.php'
            for attempt in range(100):
                try:
                    with urllib.request.urlopen(cls.base, timeout=1):
                        break
                except (OSError, urllib.error.URLError):
                    time.sleep(.05)
            else:
                raise RuntimeError('PHP test server did not start')
        except BaseException:
            cls.tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'container'):
            docker('exec', cls.container, 'sh', '-c', 'rm -rf /fixtures/state /fixtures/calls.jsonl')
            docker('rm', '-f', cls.container)
        if hasattr(cls, 'fixtures'):
            shutil.rmtree(cls.fixtures, ignore_errors=True)

    def setUp(self):
        docker('exec', self.container, 'sh', '-c', 'rm -rf /fixtures/state /fixtures/calls.jsonl')
        self.client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        status, self.config, self.headers = self.call()
        self.assertEqual(status, 200)
        self.assertTrue(self.config['ready'])

    def call(self, data=None, scenario='match', headers=None, method=None, raw=None):
        # Docker maps an ephemeral host port to 8088; use the trusted production
        # origin because its PHP SERVER_PORT intentionally differs from the host.
        options = {'Origin': 'https://www.efyseguros.com', 'X-Efy-Test-Scenario': scenario}
        if data is not None or raw is not None:
            options['Content-Type'] = 'application/json'
        options.update(headers or {})
        body = raw if raw is not None else json.dumps(data).encode() if data is not None else None
        request = urllib.request.Request(self.base, data=body, headers=options, method=method)
        try:
            response = self.client.open(request, timeout=5)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            return response.status, json.loads(response.read()), response.headers

    def valid(self):
        return {'cooperativa': 'coopartamos', 'cedula': '0000000001', 'consent': True, 'csrf': self.config['csrf']}

    def calls(self):
        path = self.fixtures / 'calls.jsonl'
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def test_response_contract_and_personal_information_boundary(self):
        status, data, headers = self.call(self.valid(), scenario='multiple')
        self.assertEqual(status, 200)
        self.assertEqual(len(data['registros']), 2)
        self.assertEqual({item['estado'] for item in data['registros']}, {'VIGENTE', 'VENCIDA'})
        self.assertIsNone(data['registros'][1]['vigencia_fin'])
        self.assertEqual(set(data), {'ok', 'encontrado', 'fecha_consulta', 'fuentes_pendientes', 'registros', 'advertencias'})
        self.assertEqual(set(data['registros'][0]), {'aseguradora', 'contrato', 'vigencia_inicio', 'vigencia_fin', 'estado'})
        response = json.dumps(data)
        for private in ['NOMBRE PRIVADO', '0000000001', '1980-01-01', 'archivo-privado', 'private-internal-id', KEY]:
            self.assertNotIn(private, response)
        self.assertEqual(self.calls(), [{'key': KEY, 'cedula': '0000000001'}])
        self.assertIn('no-store', headers['Cache-Control'])
        self.assertEqual(headers['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(docker('exec', self.container, 'stat', '-c', '%a', '/fixtures/state').strip(), '700')
        modes = docker('exec', self.container, 'sh', '-c', 'stat -c %a /fixtures/state/*').splitlines()
        self.assertTrue(modes and all(mode == '600' for mode in modes))
        saved = docker('exec', self.container, 'sh', '-c', 'cat /fixtures/state/*')
        self.assertNotIn('0000000001', saved)

    def test_no_matches_preserves_pending_privilegio(self):
        status, data, _ = self.call(self.valid(), scenario='no-match')
        self.assertEqual(status, 200)
        self.assertFalse(data['encontrado'])
        self.assertEqual(data['registros'], [])
        self.assertIn('PRIVILEGIO', data['fuentes_pendientes'])
        self.assertTrue(any('pendiente' in item for item in data['advertencias']))

    def test_upstream_failures_do_not_become_no_matches(self):
        for scenario, expected in [('unauthorized', 502), ('unavailable', 502), ('busy', 429), ('timeout', 504), ('malformed', 502), ('inconsistent', 502)]:
            with self.subTest(scenario=scenario):
                status, data, headers = self.call(self.valid(), scenario=scenario)
                self.assertEqual(status, expected)
                self.assertFalse(data['ok'])
                self.assertNotIn('registros', data)
                self.assertNotIn('encontrado', data)
                if expected == 429:
                    self.assertEqual(headers['Retry-After'], '60')

    def test_validation_and_origin_prevent_upstream_requests(self):
        for value in ['1234', 1234567890, '000000001x']:
            data = self.valid(); data['cedula'] = value
            self.assertEqual(self.call(data)[0], 422)
        for key, value, expected in [('consent', False, 422), ('cooperativa', 'otra', 422), ('csrf', 'wrong', 419)]:
            data = self.valid(); data[key] = value
            self.assertEqual(self.call(data)[0], expected)
        self.assertEqual(self.call(self.valid(), headers={'Origin': 'https://example.invalid'})[0], 403)
        self.assertEqual(self.call(self.valid(), headers={'Sec-Fetch-Site': 'cross-site'})[0], 403)
        self.assertEqual(self.call(self.valid(), headers={'Content-Type': 'text/plain'})[0], 415)
        self.assertEqual(self.call(raw=b'{invalid')[0], 400)
        self.assertEqual(self.call(raw=b'x' * 2049)[0], 413)
        self.assertEqual(self.call(method='DELETE')[0], 405)
        self.assertEqual(self.calls(), [])

    def test_rate_limit_uses_private_state(self):
        for _ in range(10):
            self.assertEqual(self.call(self.valid())[0], 200)
        status, data, headers = self.call(self.valid())
        self.assertEqual(status, 429)
        self.assertFalse(data['ok'])
        self.assertEqual(headers['Retry-After'], '900')
        self.assertEqual(len(self.calls()), 10)

    def test_missing_config_stays_unavailable_without_exposing_paths(self):
        for scenario in ['unconfigured', 'public-config', 'bad-url', 'bad-key', 'noisy-config']:
            with self.subTest(scenario=scenario):
                status, config, headers = self.call(scenario=scenario)
                self.assertEqual(status, 200)
                self.assertFalse(config['ready'])
                self.assertEqual(set(config), {'ok', 'version', 'ready', 'csrf'})
                status, data, _ = self.call(self.valid(), scenario=scenario)
                self.assertEqual(status, 503)
                self.assertNotIn('/fixtures', json.dumps(data))
                self.assertNotIn('private-config-output', json.dumps(data))
        self.assertEqual(self.calls(), [])

    def test_session_cookie_and_configuration_never_expose_credentials(self):
        self.assertEqual(set(self.config), {'ok', 'version', 'ready', 'csrf'})
        self.assertNotIn(KEY, json.dumps(self.config))
        cookie = self.headers['Set-Cookie']
        self.assertIn('HttpOnly', cookie)
        self.assertIn('SameSite=Lax', cookie)
        self.assertIn('path=/nueva/', cookie)

    def test_transport_has_fixed_secure_request_and_bounded_errors(self):
        result = docker('exec', self.container, 'php', '-d',
                        'disable_functions=curl_init,curl_setopt_array,curl_exec,curl_getinfo,curl_errno,curl_close',
                        '/site/tests/coverage/transport.php')
        self.assertIn('PASS fixed HTTPS', result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
