import pickle
import pandas as pd
from flask import Flask, render_template, request, jsonify
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Carregar o modelo treinado a partir do arquivo .pkl
with open('modelos/model_treinado.pkl', 'rb') as f:
    modelo = pickle.load(f)

normalizado = pd.read_csv("modelos/spotify_normalized.csv")
data = pd.read_csv("modelos/spotify_treated.csv")
music = pd.read_csv("modelos/spotify_cleaned.csv")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/modo_musica', methods=['POST'])
def modo_musica():
    try:
        dados = request.get_json()
        popularidade_musica = 0.5
        duracao_musica_ms = 0.5
        dancabilidade = float(dados['dancabilidade'])
        energia = float(dados['energia'])
        chave = 0.5
        vivacidade = float(dados['vivacidade'])
        volume = float(dados['volume'])
        modo_audio = float(dados['modo_audio'])
        fala = float(dados['fala'])
        ritmo = float(dados['ritmo'])
        assinatura_tempo = float(dados['assinatura_tempo'])
        valencia_audio = float(dados['valencia_audio'])

        entrada = [[popularidade_musica, duracao_musica_ms, dancabilidade, energia, chave, vivacidade, volume, modo_audio, fala, ritmo, assinatura_tempo, valencia_audio]]
        modo = modelo.predict(entrada)[0]

        return jsonify({'modo_musica': int(modo)})
    except Exception as e:
        print(f"Erro ao prever o modo de música: {e}")
        return jsonify({'erro': str(e)})

@app.route('/histograma')
def histograma():
    try:
        tipo1 = normalizado[(normalizado['modo_audio'] >= 0.0) & (normalizado['modo_audio'] < 0.0001)].shape[0]
        tipo2 = normalizado[(normalizado['modo_audio'] >= 1.0) & (normalizado['modo_audio'] < 1.0001)].shape[0]
        data = [
            {'category': 'lento', 'valor': tipo1},
            {'category': 'rapido', 'valor': tipo2},
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/graficopizza')
def graficopizza():
    try:
        key_distribution = data['key'].value_counts().to_dict()
        chart_data = [{'category': str(k), 'value': v} for k, v in key_distribution.items()]
        return jsonify(chart_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)