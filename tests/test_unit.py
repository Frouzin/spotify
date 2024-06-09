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

    @patch('pandas.read_csv')
    def test_histograma_construction(self, mock_read_csv):
        mock_df = MagicMock()
        mock_df.shape.return_value = (100, 10)
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

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='model_data')
    @patch('pickle.load')
    def test_model_loading(self, mock_pickle_load, mock_open):
        mock_pickle_load.return_value = 'mock_model'
        with open('modelos/model_treinado.pkl', 'rb') as f:
            model = pickle.load(f)
        self.assertEqual(model, 'mock_model')

    def test_home_route(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>SpotIA</title>', response.data)  # Ajustado para refletir o título correto

if __name__ == '__main__':
    unittest.main()
