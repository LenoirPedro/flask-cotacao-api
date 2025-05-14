from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <html>
        <head>
            <title>API de Cotação</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    text-align: center;
                    padding: 50px;
                }
                h1 {
                    color: #2d87f0;
                    font-size: 2.5em;
                }
                .content {
                    background-color: #fff;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 60%;
                    margin: 0 auto;
                    text-align: left;
                }
                .btn {
                    background-color: #2d87f0;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    display: inline-block;
                    margin-top: 20px;
                }
                .btn:hover {
                    background-color: #1d67c0;
                }
                footer {
                    margin-top: 30px;
                    font-size: 0.9em;
                    color: #aaa;
                }
            </style>
        </head>
        <body>
            <h1>Bem-vindo à API de Cotação</h1>
            <div class="content">
                <p>Esta API retorna a cotação em tempo real das moedas.</p>
                <p>Para verificar a cotação de uma moeda específica, use a seguinte URL:</p>
                <p><code>/cotacao?moeda=USD</code> para ver a cotação do dólar.</p>
                <a href="/cotacao?moeda=USD" class="btn">Ver cotação do Dólar</a>
            </div>
            <footer>
                <p>API desenvolvida para mostrar a cotação das moedas em tempo real.</p>
            </footer>
        </body>
    </html>
    """

@app.route("/cotacao")
def cotacao():
    moeda = request.args.get("moeda", "USD").upper()
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL"

    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return jsonify({"erro": "Falha na API externa"}), 502

        dados = resp.json()
        if f"{moeda}BRL" in dados:
            valor = float(dados[f"{moeda}BRL"]["bid"])
            return jsonify({
                "moeda": moeda,
                "cotacao_em_brl": round(valor, 2)
            })
        else:
            return jsonify({"erro": "Moeda inválida ou não encontrada"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
