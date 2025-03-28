import os
from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

API_KEY = os.getenv('OPENAI_API_KEY')
URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/perguntar', methods=['POST'])
def perguntar():
    pergunta = request.json['pergunta']

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": pergunta}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(URL, headers=HEADERS, data=json.dumps(payload))

        if response.status_code == 200:
            resposta = response.json()["choices"][0]["message"]["content"]
        elif response.status_code == 429:
            resposta = "Excedeu o limite de requisições, aguarde um pouco e tente novamente."
        else:
            resposta = f"Erro {response.status_code}: {response.text}"

    except Exception as e:
        resposta = f"Erro na requisição: {e}"

    return jsonify({'resposta': resposta})


if __name__ == '__main__':
    app.run(debug=True)
