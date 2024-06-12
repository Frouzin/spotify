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

    def test_home_page_elements(self):
        self.driver.get('http://localhost:5000')
        element = self.driver.find_element_by_id('some_element_id')
        self.assertIsNotNone(element)

    def test_home_page_links(self):
        self.driver.get('http://localhost:5000')
        links = self.driver.find_elements_by_tag_name('a')
        self.assertGreater(len(links), 0)

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

    def test_post_valid_data_to_modo_musica_diferente(self):
        self.driver.get('http://localhost:5000')
        data = {
            'dancabilidade': 0.7,
            'energia': 0.8,
            'vivacidade': 0.9,
            'volume': -3,
            'modo_audio': 0,
            'fala': 0.3,
            'ritmo': 130,
            'assinatura_tempo': 3,
            'valencia_audio': 0.8
        }
        response = self.driver.execute_script('return fetch("/modo_musica", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(arguments[0])}).then(res => res.json())', data)
        self.assertIn('modo_musica', response)

    def test_post_valid_data_to_modo_musica_extremo(self):
        self.driver.get('http://localhost:5000')
        data = {
            'dancabilidade': 1.0,
            'energia': 1.0,
            'vivacidade': 1.0,
            'volume': 0,
            'modo_audio': 1,
            'fala': 0.0,
            'ritmo': 240,
            'assinatura_tempo': 4,
            'valencia_audio': 1.0
        }
        response = self.driver.execute_script('return fetch("/modo_musica", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(arguments[0])}).then(res => res.json())', data)
        self.assertIn('modo_musica', response)

    def test_post_invalid_data_to_modo_musica(self):
        self.driver.get('http://localhost:5000')
        data = {}
        response = self.driver.execute_script('return fetch("/modo_musica", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(arguments[0])}).then(res => res.json())', data)
        self.assertIn('erro', response)

    def test_post_invalid_data_to_modo_musica_texto(self):
        self.driver.get('http://localhost:5000')
        data = {
            'dancabilidade': 'texto',
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
        self.assertIn('erro', response)

    def test_post_invalid_data_to_modo_musica_faltando_campo(self):
        self.driver.get('http://localhost:5000')
        data = {
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
        self.assertIn('erro', response)

    def test_get_histograma_data(self):
        self.driver.get('http://localhost:5000/histograma')
        response = self.driver.execute_script('return fetch("/histograma").then(res => res.json())')
        self.assertIsInstance(response, list)

    def test_get_histograma_data_vazia(self):
        # Supondo que você possa configurar a aplicação para retornar um histograma vazio
        self.driver.get('http://localhost:5000/histograma?vazia=true')
        response = self.driver.execute_script('return fetch("/histograma?vazia=true").then(res => res.json())')
        self.assertEqual(len(response), 0)

    def test_get_histograma_data_completa(self):
        # Supondo que você possa configurar a aplicação para retornar um histograma completo
        self.driver.get('http://localhost:5000/histograma?completa=true')
        response = self.driver.execute_script('return fetch("/histograma?completa=true").then(res => res.json())')
        self.assertGreater(len(response), 0)

    def test_get_graficopizza_data(self):
        self.driver.get('http://localhost:5000/graficopizza')
        response = self.driver.execute_script('return fetch("/graficopizza").then(res => res.json())')
        self.assertIsInstance(response, list)

    def test_get_graficopizza_data_vazia(self):
        # Supondo que você possa configurar a aplicação para retornar um gráfico de pizza vazio
        self.driver.get('http://localhost:5000/graficopizza?vazia=true')
        response = self.driver.execute_script('return fetch("/graficopizza?vazia=true").then(res => res.json())')
        self.assertEqual(len(response), 0)

    def test_get_graficopizza_data_completa(self):
        # Supondo que você possa configurar a aplicação para retornar um gráfico de pizza completo
        self.driver.get('http://localhost:5000/graficopizza?completa=true')
        response = self.driver.execute_script('return fetch("/graficopizza?completa=true").then(res => res.json())')
        self.assertGreater(len(response), 0)

if __name__ == '__main__':
    unittest.main()
