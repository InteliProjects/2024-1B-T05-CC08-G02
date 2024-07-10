from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import sys
import os
import requests
#pip install flask
#pip install flask-cors
# Adiciona o caminho do diretório 'lexico' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../compilador')))

# Agora você pode importar o AnalisadorLexico
from AnalisadorLexico import AnalisadorLexico
from AnalisadorSintatico import AnalisadorSintatico
from AnalisadorSemantico import AnalisadorSemantico
from GeradorCodigo import GeradorCodigo
app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS jogos2 (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            terapeuta TEXT NOT NULL,
                            paciente TEXT NOT NULL,
                            projeto TEXT NOT NULL,
                            codigoFonte TEXT NOT NULL
                        )''')
        db.commit()

init_db()
@app.route('/run-python-code', methods=['POST', 'OPTIONS'])
def run_python_code():
    # Se a solicitação for OPTIONS, responde com headers permitindo origens cruzadas
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    # Se a solicitação for POST, analisa o código fornecido e retorna a saída ou um erro
    elif request.method == 'POST':
        # Obtém o JSON enviado na solicitação POST
        data = request.get_json(force=True)
        # Obtém o código a ser analisado do JSON
        code = data.get('code')
        url = 'https://servidor-pessoal.onrender.com/verifica'
        response = requests.post(url, json=code)
        if response.status_code == 200:
            response_data = response.json()
            js_code = response_data.get('response')
            response = jsonify({'output': js_code})
            # Adiciona headers permitindo origens cruzadas à resposta
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
@app.route('/gerar', methods=['POST', 'OPTIONS'])
def gerar():
    # Se a solicitação for OPTIONS, responde com headers permitindo origens cruzadas
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    # Se a solicitação for POST, analisa o código fornecido e retorna a saída ou um erro
    elif request.method == 'POST':
        # Obtém o JSON enviado na solicitação POST
        data = request.get_json(force=True)
        # Obtém o código a ser analisado do JSON
        code = data.get('code')
        analisador1=AnalisadorLexico
        analisador2=AnalisadorSintatico
        analisador3=AnalisadorSemantico
        gerador=GeradorCodigo
        url = 'http://servidor-pessoal.onrender.com/gerar'
        response = requests.post(url, json=code)
        if response.status_code == 200:
            response_data = response.json()
            js_code = response_data.get('response')
            response = jsonify({'output': js_code})
            response.headers.add('Access-Control-Allow-Origin', '*')
            if js_code:
                with open('..\\jogo\\programa.js', 'w') as file:
                    file.write(js_code)
                print("Código JS salvo em output.js")
                return response
            else:
                print("Erro: Resposta da API não contém 'response'")
        else:
            print(f"Erro: {response.status_code}, {response.text}")
@app.route('/save-data', methods=['POST'])
def save_data():
    if request.method == 'POST':
        data = request.json

        terapeuta = data.get('terapeuta')
        paciente = data.get('paciente')
        projeto = data.get('projeto')
        codigoFonte = data.get('codigoFonte')

        try:
            with sqlite3.connect('database.db', timeout=10) as db:
                cursor = db.cursor()
                sql = "INSERT INTO jogos2 (terapeuta, paciente, projeto, codigoFonte) VALUES (?, ?, ?, ?)"
                cursor.execute(sql, (terapeuta, paciente, projeto, codigoFonte))
                db.commit()
                last_id = cursor.lastrowid

            return jsonify({'status': 'success', 'message': 'Dados salvos com sucesso!', 'id': last_id})
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                return jsonify({'status': 'error', 'message': 'Database is currently locked, please try again later.'})
            else:
                return jsonify({'status': 'error', 'message': str(e)})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get-data', methods=['GET'])
def get_data():
    try:
        with sqlite3.connect('database.db', timeout=10) as db:
            cursor = db.cursor()
            cursor.execute("SELECT id, terapeuta, paciente, projeto, codigoFonte FROM jogos2")
            rows = cursor.fetchall()

            data = []
            for row in rows:
                data.append({
                    'id': row[0],
                    'terapeuta': row[1],
                    'paciente': row[2],
                    'projeto': row[3],
                    'codigoFonte': row[4]
                })

        return jsonify({'status': 'success', 'data': data})
    except sqlite3.OperationalError as e:
        if 'database is locked' in str(e):
            return jsonify({'status': 'error', 'message': 'Database is currently locked, please try again later.'})
        else:
            return jsonify({'status': 'error', 'message': str(e)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
