from flask_testing import TestCase
from app import app

class TestAppIntegration(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_modo_musica_integration(self):
        response = self.client.post('/modo_musica', json={
            'dancabilidade': 0.5,
            'energia': 0.6,
            'vivacidade': 0.7,
            'volume': -5,
            'modo_audio': 1,
            'fala': 0.2,
            'ritmo': 120,
            'assinatura_tempo': 4,
            'valencia_audio': 0.9
        })
        self.assert200(response)
        self.assertIn('modo_musica', response.json)

    def test_histograma_integration(self):
        response = self.client.get('/histograma')
        self.assert200(response)
        self.assertIsInstance(response.json, list)

    def test_graficopizza_integration(self):
        response = self.client.get('/graficopizza')
        self.assert200(response)
        self.assertIsInstance(response.json, list)

    def test_valid_json_response(self):
        response = self.client.post('/modo_musica', json={
            'dancabilidade': 0.5,
            'energia': 0.6,
            'vivacidade': 0.7,
            'volume': -5,
            'modo_audio': 1,
            'fala': 0.2,
            'ritmo': 120,
            'assinatura_tempo': 4,
            'valencia_audio': 0.9
        })
        self.assert200(response)
        self.assertEqual(response.content_type, 'application/json')

    def test_invalid_data_response(self):
        response = self.client.post('/modo_musica', json={})
        self.assert500(response)  # O código de status esperado é 500
        self.assertIn('erro', response.json)

if __name__ == '__main__':
    unittest.main()
