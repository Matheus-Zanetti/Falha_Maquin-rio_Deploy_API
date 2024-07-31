import pandas as pd
from flask import Flask, request, jsonify
import joblib
import logging


app = Flask(__name__)

# Carregar o modelo treinado
modelo = joblib.load('Prev_Maq.pkl')

@app.route('/')
def home():
    return "Teste API"

@app.route('/prev_maq', methods=['POST'])
def prev_maq():
    logging.info("Iniciando previsão da máquina")
    try:
        dados_input = request.get_json()
        dados_df = pd.DataFrame([dados_input])
        # Verifique se as colunas necessárias estão presentes
        colunas_necessarias = ['footfall', 'tempMode', 'AQ', 'USS', 'CS', 'VOC', 'RP', 'IP','Temperature']
        for coluna in colunas_necessarias:
            if coluna not in dados_df.columns:
                return jsonify({'erro': f'Coluna {coluna} está faltando nos dados de entrada'}), 400
        
        # Faça a previsão
        prev_maq = modelo.predict(dados_df)

        previsao = []
        for resultado in prev_maq:
            if resultado == 0:
                previsao.append(f'Retorno {resultado}: Máquina Operando Normalmente')
            else:
                previsao.append(f'Retorno {resultado}: Máquina Operando com Expectativa de falha')
        return jsonify({'previsao': previsao})
    except Exception as e:
        logging.error(f"Erro durante a previsão: {str(e)}")
        return jsonify({'erro': str(e)}), 500

app.run(debug=True)
