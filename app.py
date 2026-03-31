from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

from utils import carregar_processos, salvar_processos, converter_para_iso
from services.prazo_service import calcular_prazo

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/processos", methods=["GET"])
def listar_processos():
    processos = carregar_processos()
    return jsonify({
        "sucesso": True,
        "dados": processos
    })


@app.route("/processos", methods=["POST"])
def criar_processo():
    data = request.json

    numero = data.get("numero")
    nome = data.get("nome")
    data_inicial = data.get("data_inicial")
    dias = data.get("dias")

    if not numero or not isinstance(numero, str):
        return jsonify({
            "sucesso": False,
            "erro": "Número inválido"
        }), 400

    if not dias or not str(dias).isdigit():
        return jsonify({
            "sucesso": False,
            "erro": "Dias inválido"
        }), 400

    processos = carregar_processos()

    if any(p["numero"] == numero for p in processos):
        return jsonify({
            "sucesso": False,
            "erro": "Processo já existe"
        }), 400

    try:
        data_iso = converter_para_iso(data_inicial)
    except:
        return jsonify({
            "sucesso": False,
            "erro": "Data inválida"
        }), 400

    prazo_final = calcular_prazo(data_iso, int(dias))

    novo = {
        "numero": numero,
        "nome": nome,
        "prazo": prazo_final
    }

    processos.append(novo)
    salvar_processos(processos)

    return jsonify({
        "sucesso": True,
        "dados": novo
    }), 201


@app.route("/processos/<numero>", methods=["GET"])
def buscar_processo(numero):
    processos = carregar_processos()

    for p in processos:
        if p["numero"] == numero:
            return jsonify({
                "sucesso": True,
                "dados": p
            })

    return jsonify({
        "sucesso": False,
        "erro": "Não encontrado"
    }), 404


@app.route("/processos/<numero>", methods=["DELETE"])
def deletar_processo(numero):
    processos = carregar_processos()

    novos = [p for p in processos if p["numero"] != numero]

    if len(processos) == len(novos):
        return jsonify({
            "sucesso": False,
            "erro": "Não encontrado"
        }), 404

    salvar_processos(novos)

    return jsonify({
        "sucesso": True,
        "mensagem": "Processo removido com sucesso"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)