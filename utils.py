import json

ARQUIVO = "processos.json"


def carregar_processos():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except:
        return []


def salvar_processos(processos):
    with open(ARQUIVO, "w") as f:
        json.dump(processos, f, indent=4)

from datetime import datetime


def converter_para_iso(data_str):
    return datetime.strptime(data_str, "%d/%m/%Y").strftime("%Y-%m-%d")


def converter_para_br(data_str):
    return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")


def calcular_prioridade(prazo_iso):
    hoje = datetime.today()
    prazo_data = datetime.strptime(prazo_iso, "%Y-%m-%d")
    dias_restantes = (prazo_data - hoje).days
    
    if dias_restantes <= 3:
        return "🔴 URGENTE"
    elif dias_restantes <= 7:
        return "🟡 Normal"
    else:
        return "🟢 Baixa"