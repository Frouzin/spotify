import unittest
from selenium import webdriver

class TestAppSystem(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_home_page_load(self):
        self.driver.get('http://localhost:5000')
        self.assertIn('SpotIA', self.driver.title)  # Ajustado para refletir o título correto

    def test_post_valid_data_to_modo_musica(self):
        self.driver.get('http://localhost:5000')
        data = {
            'dancabilidade': 0.5,
            'energia': 0.6,
            'vivacidade': 0.7,
            'volume': -5,
            'modo_audio': 1,
            'fala': 0.2,
            'ritmo': 120,
            'assinatura_tempo': 4,
            'valencia_audio': 0.9
        }
        response = self.driver.execute_script('return fetch("/modo_musica", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(arguments[0])}).then(res => res.json())', data)
        self.assertIn('modo_musica', response)

    def test_post_invalid_data_to_modo_musica(self):
        self.driver.get('http://localhost:5000')
        data = {}
        response = self.driver.execute_script('return fetch("/modo_musica", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(arguments[0])}).then(res => res.json())', data)
        self.assertIn('erro', response)

    def test_get_histograma_data(self):
        self.driver.get('http://localhost:5000/histograma')
        response = self.driver.execute_script('return fetch("/histograma").then(res => res.json())')
        self.assertIsInstance(response, list)

    def test_get_graficopizza_data(self):
        self.driver.get('http://localhost:5000/graficopizza')
        response = self.driver.execute_script('return fetch("/graficopizza").then(res => res.json())')
        self.assertIsInstance(response, list)

if __name__ == '__main__':
    unittest.main()
