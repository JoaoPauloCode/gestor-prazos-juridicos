import json
from datetime import datetime

ARQUIVO = "processos.json"


def carregar_processos():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def salvar_processos(processos):
    with open(ARQUIVO, "w") as f:
        json.dump(processos, f, indent=4)


def converter_para_iso(data_str):
    return datetime.strptime(data_str, "%d/%m/%Y").strftime("%Y-%m-%d")


def converter_para_br(data_str):
    return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")