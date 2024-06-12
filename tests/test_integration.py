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
        
        
    def test_modo_musica_baixa_fala(self):
        response = self.client.post('/modo_musica', json={
            'dancabilidade': 0.5,
            'energia': 0.6,
            'vivacidade': 0.7,
            'volume': -5,
            'modo_audio': 1,
            'fala': 0.1,
            'ritmo': 120,
            'assinatura_tempo': 4,
            'valencia_audio': 0.9
        })
        self.assert200(response)
        self.assertIn('modo_musica', response.json)

    def test_modo_musica_alto_ritmo(self):
        response = self.client.post('/modo_musica', json={
            'dancabilidade': 0.5,
            'energia': 0.6,
            'vivacidade': 0.7,
            'volume': -5,
            'modo_audio': 1,
            'fala': 0.2,
            'ritmo': 200,
            'assinatura_tempo': 4,
            'valencia_audio': 0.9
        })
        self.assert200(response)
        self.assertIn('modo_musica', response.json)

    def test_histograma_integration(self):
        response = self.client.get('/histograma')
        self.assert200(response)
        self.assertIsInstance(response.json, list)
        
    def test_histograma_vazio(self):
        # Assumindo que você pode configurar a aplicação para retornar um histograma vazio
        response = self.client.get('/histograma?data=')
        self.assert200(response)
        self.assertEqual(len(response.json), 0)

    def test_histograma_com_dados(self):
        # Assumindo que você pode passar dados diretamente para o histograma via URL
        response = self.client.get('/histograma?data=1,2,3,4,5')
        self.assert200(response)
        self.assertEqual(len(response.json), 5)

    def test_graficopizza_integration(self):
        response = self.client.get('/graficopizza')
        self.assert200(response)
        self.assertIsInstance(response.json, list)
    
    def test_graficopizza_vazio(self):
        response = self.client.get('/graficopizza?labels=&sizes=')
        self.assert200(response)
        self.assertEqual(len(response.json), 0)

    def test_graficopizza_com_dados(self):
        response = self.client.get('/graficopizza?labels=A,B,C&sizes=10,20,30')
        self.assert200(response)
        self.assertEqual(len(response.json), 3)

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
        
    def test_valid_json_response_histograma(self):
        response = self.client.get('/histograma')
        self.assert200(response)
        self.assertEqual(response.content_type, 'application/json')

    def test_valid_json_response_graficopizza(self):
        response = self.client.get('/graficopizza')
        self.assert200(response)
        self.assertEqual(response.content_type, 'application/json')

    def test_invalid_data_response(self):
        response = self.client.post('/modo_musica', json={})
        self.assert500(response)  # O código de status esperado é 500
        self.assertIn('erro', response.json)

    def test_invalid_data_response_tipo_errado(self):
        response = self.client.post('/modo_musica', json={'dancabilidade': 'texto'})
        self.assert400(response)
        self.assertIn('erro', response.json)

    def test_invalid_data_response_falta_dado(self):
        response = self.client.post('/modo_musica', json={'energia': 0.6})
        self.assert400(response)
        self.assertIn('erro', response.json)

if __name__ == '__main__':
    unittest.main()
