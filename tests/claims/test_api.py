"""Integration checks against isolated PHP containers with a fake mail transport.

Only localhost test servers and the specifically named test containers are used.
Never invoke these checks against production or with a real mail transport.
"""
import base64
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import email
from email import policy
import http.cookiejar
import json
import os
import subprocess
import unittest
import urllib.error
import urllib.request
import uuid

DOCKER = ['docker', '--host=unix:///var/run/docker.sock']
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/l9sAAAAASUVORK5CYII=')


def docker(*args):
    env = os.environ.copy()
    for name in ['DOCKER_HOST','DOCKER_CONTEXT','DOCKER_TLS','DOCKER_TLS_VERIFY','DOCKER_CERT_PATH']:
        env.pop(name, None)
    return subprocess.check_output(DOCKER + list(args), env=env, text=True)


def payload():
    return {'name':'Cliente de prueba','phone':'+593 99 123 4567','email':'cliente@example.invalid',
            'insurer':'Aseguradora de prueba','policy':'PRUEBA-001','event_type':'Daños',
            'event_date':datetime.now(ZoneInfo('America/Guayaquil')).date().isoformat(),'event_time':'12:30','location':'Quito, ubicación de prueba',
            'description':'Este reporte es una prueba técnica del formulario. No corresponde a un siniestro real.',
            'consent':'1','website':'','request_id':str(uuid.uuid4())}


def multipart(values, files=()):
    boundary='test_'+uuid.uuid4().hex
    body=bytearray()
    for key,value in values.items():
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'.encode())
    for name,content,kind in files:
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="attachments[]"; filename="{name}"\r\nContent-Type: {kind}\r\n\r\n'.encode())
        body.extend(content);body.extend(b'\r\n')
    body.extend(f'--{boundary}--\r\n'.encode())
    return bytes(body), 'multipart/form-data; boundary='+boundary


class ClaimIntake(unittest.TestCase):
    def setUp(self):
        for container in ['efy-claims-test','efy-claims-fail']:
            # Both containers have test-only mail capture. Do not permit accidental real transport.
            configured=json.loads(docker('inspect',container))[0]['Config']['Cmd']
            self.assertIn('sendmail_path=/tests/fake-sendmail.sh', configured)
            docker('exec',container,'sh','-c','rm -rf /tmp/efy-state /tmp/efy-test-mail')
        self.client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.base='http://127.0.0.1:8088/nueva/api/siniestros.php'
        code, self.config=self.call()
        self.assertEqual(code,200)
        self.assertTrue(self.config['ready'])
        self.assertEqual(self.config['recipient'],'siniestros@efyseguros.com')

    def call(self, values=None, files=(), headers=None, method=None, target=None):
        body,kind=multipart(values,files) if values is not None else (None,None)
        options={'Origin':'http://127.0.0.1:8088'}
        if kind: options['Content-Type']=kind
        options.update(headers or {})
        request=urllib.request.Request(target or self.base,data=body,headers=options,method=method)
        try: response=self.client.open(request,timeout=10)
        except urllib.error.HTTPError as error: response=error
        with response:return response.status,json.loads(response.read())

    def valid(self):
        data=payload();data['csrf']=self.config['csrf'];return data

    def messages(self,container='efy-claims-test'):
        return docker('exec',container,'sh','-c','cat /tmp/efy-test-mail 2>/dev/null || true')

    def test_mail_and_attachment_and_private_retry_metadata(self):
        data=self.valid()
        code,result=self.call(data,[('evil-name.php',PNG,'image/png')])
        self.assertEqual(code,200);self.assertTrue(result['ok'])
        self.assertRegex(result['reference'],r'^EFY-\d{8}-[A-F0-9]{10}$')
        message=email.message_from_string(self.messages().split('--EFY-TEST-MESSAGE--')[0],policy=policy.default)
        self.assertEqual(message['To'],'siniestros@efyseguros.com')
        self.assertEqual(message['Reply-To'],'cliente@example.invalid')
        text=message.get_body(preferencelist=('plain',)).get_content()
        self.assertIn('Cliente de prueba',text)
        self.assertIn(result['reference'],text)
        attachment=list(message.iter_attachments())[0]
        self.assertEqual(attachment.get_filename(),'adjunto-1.png')
        self.assertEqual(attachment.get_payload(decode=True),PNG)
        state=docker('exec','efy-claims-test','sh','-c','cat /tmp/efy-state/request-*.json')
        self.assertNotIn('Cliente de prueba',state)
        self.assertNotIn('cliente@example.invalid',state)
        self.assertNotIn('PRUEBA-001',state)
        mode=docker('exec','efy-claims-test','stat','-c','%a','/tmp/efy-state').strip()
        self.assertEqual(mode,'700')

    def test_retry_does_not_send_twice_and_changed_payload_is_rejected(self):
        data=self.valid()
        code,first=self.call(data)
        self.assertEqual(code,200)
        code,retry=self.call(data)
        self.assertEqual(code,200);self.assertEqual(first['reference'],retry['reference'])
        self.assertEqual(self.messages().count('--EFY-TEST-MESSAGE--'),1)
        data['description']='Este es otro reporte con información diferente para el mismo intento.'
        code,result=self.call(data)
        self.assertEqual(code,409);self.assertFalse(result['ok'])
        self.assertEqual(self.messages().count('--EFY-TEST-MESSAGE--'),1)

    def test_validation_and_csrf_and_origin_prevent_mail(self):
        data=self.valid()
        data.update(name=' ',phone='abc',email='cliente@example.invalid\r\nBcc:otro@example.invalid',event_date=(datetime.now(ZoneInfo('America/Guayaquil')).date()+timedelta(days=1)).isoformat(),description='corto',consent='0')
        code,result=self.call(data)
        self.assertEqual(code,422)
        self.assertTrue({'name','phone','email','event_date','description','consent'} <= set(result['errors']))
        data=self.valid();data['csrf']='invalid'
        self.assertEqual(self.call(data)[0],419)
        self.assertEqual(self.call(self.valid(),headers={'Origin':'https://unrelated.example.invalid'})[0],403)
        self.assertEqual(self.call(method='DELETE')[0],405)
        self.assertEqual(self.messages(),'')

    def test_bad_and_oversized_and_excess_files_are_rejected(self):
        for files in [[('script.jpg',b'<?php echo "bad";?>','image/jpeg')],
                      [('big.png',PNG+b'X'*2097152,'image/png')],
                      [('picture.png',PNG,'image/png')]*4]:
            code,result=self.call(self.valid(),files)
            self.assertEqual(code,422)
            self.assertIn('attachments',result['errors'])
        self.assertEqual(self.messages(),'')

    def test_mail_failure_never_confirms_receipt(self):
        target='http://127.0.0.1:8089/nueva/api/siniestros.php'
        _,config=self.call(target=target)
        data=self.valid();data['csrf']=config['csrf']
        code,result=self.call(data,target=target)
        self.assertEqual(code,503)
        self.assertFalse(result['ok']);self.assertNotIn('received_at',result)

    def test_rate_limit(self):
        for _ in range(10):
            self.assertEqual(self.call(self.valid())[0],200)
        code,result=self.call(self.valid())
        self.assertEqual(code,429);self.assertFalse(result['ok'])
        self.assertEqual(self.messages().count('--EFY-TEST-MESSAGE--'),10)


if __name__=='__main__':unittest.main(verbosity=2)
