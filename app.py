from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

