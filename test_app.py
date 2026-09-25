import os
os.environ['COOKIE_SECURE']='false'
os.environ.pop('OPENAI_API_KEY',None)
import unittest
from unittest.mock import patch
import app as module

P=dict(branch='Army',role='92Y Supply Specialist',years='6',responsibilities='Tracked inventory',education='Business degree',interests='logistics',collaboration='With a team',structure='Clear routines',focus='Systems and data',environment='Hybrid')

class PrivacyTests(unittest.TestCase):
    def setUp(self):
        module.sessions.clear();module.profiles.clear()
        self.c=module.app.test_client();self.c.get('/')
        self.token=self.c.get('/api/session').json['csrf']
    def post(self, **changes):
        body=dict(profile=P.copy(),consent=True,mode='demo',ai_consent=False);body.update(changes)
        return self.c.post('/api/generate',json=body,headers={'X-CSRF-Token':self.token})
    def test_complete_flow(self):
        r=self.post();self.assertEqual(r.status_code,200);self.assertEqual(len(r.json['results']['careers']),3)
        module.validate(r.json['results'],module.SCHEMA)
        self.assertEqual(self.c.get('/api/export').json['profile']['role'],P['role'])
        self.assertEqual(self.c.delete('/api/profile',headers={'X-CSRF-Token':self.token}).status_code,200)
        self.assertEqual(module.profiles,{})
        self.assertEqual(self.c.get('/api/export').status_code,401)
    def test_isolation(self):
        self.post();other=module.app.test_client();other.get('/')
        self.assertEqual(other.get('/api/export').json,{})
        self.assertNotEqual(other.get('/api/session').json['csrf'],self.token)
    def test_csrf_and_consent(self):
        self.assertEqual(self.c.post('/api/generate',json={}).status_code,403)
        self.assertEqual(self.post(consent=False).status_code,400)
        self.assertEqual(self.post(mode='ai').status_code,400)
    def test_input_rejection(self):
        for value in ['123-45-6789','SSN 123456789','my@email.com','DoD ID 1234567890','PTSD diagnosis']:
            self.assertEqual(self.post(profile={**P,'responsibilities':value}).status_code,400)
        self.assertEqual(self.post(profile={**P,'name':'Someone'}).status_code,400)
        self.assertEqual(self.post(profile={**P,'years':'-1'}).status_code,400)
        self.assertEqual(self.post(profile={**P,'role':'x'*151}).status_code,400)
    def test_sanitization(self):
        r=self.post(profile={**P,'responsibilities':'<script>hello</script>\x00world'})
        self.assertEqual(r.json['profile']['responsibilities'],'hello world')
    def test_expiry(self):
        self.post()
        for meta in module.sessions.values():meta['expires']=0
        self.assertEqual(self.c.get('/api/export').status_code,401);self.assertEqual(module.profiles,{})
    def test_rate_limit(self):
        for _ in range(10):self.assertEqual(self.post().status_code,200)
        self.assertEqual(self.post().status_code,429)
    def test_provider_failure_fallback(self):
        with patch.dict(os.environ,{'OPENAI_API_KEY':'fake'}),patch.object(module,'generate_ai',side_effect=RuntimeError()):
            r=self.post(mode='ai',ai_consent=True)
        self.assertEqual(r.json['source'],'demo');self.assertIn('unavailable',r.json['notice'])
    def test_delete_during_generation(self):
        def delete_while_generating(p):
            with module.lock:
                module.sessions.clear();module.profiles.clear()
            return module.demo(p)
        with patch.dict(os.environ,{'OPENAI_API_KEY':'fake'}),patch.object(module,'generate_ai',side_effect=delete_while_generating):
            self.assertEqual(self.post(mode='ai',ai_consent=True).status_code,409)
        self.assertEqual(module.profiles,{})
    def test_headers_and_cookie(self):
        r=self.c.get('/')
        self.assertIn('HttpOnly',r.headers['Set-Cookie']);self.assertIn('SameSite=Strict',r.headers['Set-Cookie'])
        self.assertEqual(r.headers['Cache-Control'],'no-store')
        self.assertIn("default-src 'self'",r.headers['Content-Security-Policy'])

if __name__=='__main__':unittest.main()
