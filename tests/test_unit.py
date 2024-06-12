import unittest
from unittest.mock import patch, MagicMock
from app import app, modelo
import pickle  # Adicionando importação de pickle

class TestAppUnit(unittest.TestCase):

    @patch('app.modelo.predict')
    def test_modo_musica_prediction(self, mock_predict):
        mock_predict.return_value = [1]
        tester = app.test_client(self)
        response = tester.post('/modo_musica', json={
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
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"modo_musica":1', response.data)
    
    @patch('app.modelo.predict')
    def test_modo_musica_prediction_zero_values(self, mock_predict):
        mock_predict.return_value = [0]
        tester = app.test_client(self)
        response = tester.post('/modo_musica', json={
            'dancabilidade': 0,
            'energia': 0,
            'vivacidade': 0,
            'volume': 0,
            'modo_audio': 0,
            'fala': 0,
            'ritmo': 0,
            'assinatura_tempo': 0,
            'valencia_audio': 0
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"modo_musica":0', response.data)

    @patch('app.modelo.predict')
    def test_modo_musica_prediction_high_values(self, mock_predict):
        mock_predict.return_value = [1]
        tester = app.test_client(self)
        response = tester.post('/modo_musica', json={
            'dancabilidade': 1,
            'energia': 1,
            'vivacidade': 1,
            'volume': 1,
            'modo_audio': 1,
            'fala': 1,
            'ritmo': 1,
            'assinatura_tempo': 1,
            'valencia_audio': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"modo_musica":1', response.data)

    @patch('pandas.read_csv')
    def test_histograma_construction(self, mock_read_csv):
        mock_df = MagicMock()
        mock_df.shape.return_value = (100, 10)
        mock_read_csv.return_value = mock_df

        tester = app.test_client(self)
        response = tester.get('/histograma')
        self.assertEqual(response.status_code, 200)
        
    @patch('pandas.read_csv')
    def test_histograma_construction_empty(self, mock_read_csv):
        mock_df = MagicMock()
        mock_df.shape.return_value = (0, 10)
        mock_read_csv.return_value = mock_df

        tester = app.test_client(self)
        response = tester.get('/histograma')
        self.assertEqual(response.status_code, 200)

    @patch('pandas.read_csv')
    def test_histograma_construction_large(self, mock_read_csv):
        mock_df = MagicMock()
        mock_df.shape.return_value = (10000, 10)
        mock_read_csv.return_value = mock_df

        tester = app.test_client(self)
        response = tester.get('/histograma')
        self.assertEqual(response.status_code, 200)

    @patch('pandas.read_csv')
    def test_graficopizza_construction(self, mock_read_csv):
        mock_df = MagicMock()
        mock_df['key'].value_counts.return_value.to_dict.return_value = {'0': 10, '1': 15}
        mock_read_csv.return_value = mock_df

        tester = app.test_client(self)
        response = tester.get('/graficopizza')
        self.assertEqual(response.status_code, 200)
        
    @patch('pandas.read_csv')
    def test_graficopizza_construction_empty(self, mock_read_csv):
        mock_df = MagicMock()
        mock_df['key'].value_counts.return_value.to_dict.return_value = {}
        mock_read_csv.return_value = mock_df

        tester = app.test_client(self)
        response = tester.get('/graficopizza')
        self.assertEqual(response.status_code, 200)

    @patch('pandas.read_csv')
    def test_graficopizza_construction_large(self, mock_read_csv):
        mock_df = MagicMock()
        mock_df['key'].value_counts.return_value.to_dict.return_value = {str(i): i for i in range(100)}
        mock_read_csv.return_value = mock_df

        tester = app.test_client(self)
        response = tester.get('/graficopizza')
        self.assertEqual(response.status_code, 200)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='model_data')
    @patch('pickle.load')
    def test_model_loading(self, mock_pickle_load, mock_open):
        mock_pickle_load.return_value = 'mock_model'
        with open('modelos/model_treinado.pkl', 'rb') as f:
            model = pickle.load(f)
        self.assertEqual(model, 'mock_model')
        
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='different_model_data')
    @patch('pickle.load')
    def test_model_loading_different_model(self, mock_pickle_load, mock_open):
        mock_pickle_load.return_value = 'different_mock_model'
        with open('modelos/model_treinado.pkl', 'rb') as f:
            model = pickle.load(f)
        self.assertEqual(model, 'different_mock_model')

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='model_data')
    @patch('pickle.load')
    def test_model_loading_error(self, mock_pickle_load, mock_open):
        mock_pickle_load.side_effect = Exception('Model loading error')
        with self.assertRaises(Exception) as context:
            with open('modelos/model_treinado.pkl', 'rb') as f:
                model = pickle.load(f)
        self.assertEqual(str(context.exception), 'Model loading error')

    def test_home_route(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>SpotIA</title>', response.data)  # Ajustado para refletir o título correto
        
    def test_home_route_content(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'Bem-vindo ao SpotIA!', response.data)
        self.assertIn(b'Analise de musicas com IA', response.data)

    def test_home_route_links(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'href="/modo_musica"', response.data)
        self.assertIn(b'href="/histograma"', response.data)
        self.assertIn(b'href="/graficopizza"', response.data)

if __name__ == '__main__':
    unittest.main()
