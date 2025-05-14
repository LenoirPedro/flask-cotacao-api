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
            return render_error("Falha na API externa"), 502

        dados = resp.json()
        key = f"{moeda}BRL"
        if key in dados:
            valor = float(dados[key]["bid"])
            nome = dados[key]["name"]
            return render_html(moeda, valor, nome)
        else:
            return render_error("Moeda inválida ou não encontrada"), 400
    except Exception as e:
        return render_error(str(e)), 500

def render_html(moeda, valor, nome):
    return f"""
    <html>
        <head>
            <title>Cotação de {moeda}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(to right, #e3f2fd, #ffffff);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                .card {{
                    background-color: white;
                    border-radius: 12px;
                    padding: 40px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 400px;
                    width: 100%;
                }}
                .icon {{
                    font-size: 3em;
                    color: #2d87f0;
                }}
                h2 {{
                    margin: 10px 0;
                    color: #2d87f0;
                }}
                p {{
                    font-size: 1.2em;
                    color: #333;
                }}
            </style>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        </head>
        <body>
            <div class="card">
                <div class="icon">
                    <i class="fas fa-money-bill-wave"></i>
                </div>
                <h2>{nome}</h2>
                <p><strong>Moeda:</strong> {moeda}</p>
                <p><strong>Valor em BRL:</strong> R$ {valor:.2f}</p>
            </div>
        </body>
    </html>
    """

def render_error(mensagem):
    return f"""
    <html>
        <head>
            <title>Erro</title>
            <style>
                body {{
                    font-family: Arial;
                    background-color: #fff0f0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                .card {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
                    text-align: center;
                    color: red;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Erro</h2>
                <p>{mensagem}</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
