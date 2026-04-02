import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO = os.path.join(BASE_DIR, "processos.json")


def carregar_processos():
    if not os.path.exists(CAMINHO):
        return []

    with open(CAMINHO, "r") as f:
        return json.load(f)


def salvar_processos(processos):
    with open(CAMINHO, "w") as f:
        json.dump(processos, f, indent=4)


def converter_para_iso(data_str):
    return datetime.strptime(data_str, "%Y-%m-%d").strftime("%Y-%m-%d")