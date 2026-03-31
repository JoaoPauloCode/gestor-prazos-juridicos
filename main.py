from utils import (
    carregar_processos,
    salvar_processos,
    converter_para_iso,
    converter_para_br
)

from services.prazo_service import calcular_prazo
from datetime import datetime


def menu():
    while True:
        print("\n" + "=" * 30)
        print("GESTOR DE PRAZOS")
        print("=" * 30)
        print("1 - Cadastrar processo")
        print("2 - Listar processos")
        print("3 - Buscar processo")
        print("4 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            numero = input("Número do processo: ")
            nome = input("Nome da parte: ")

            # validar data
            while True:
                data_input = input("Data inicial (DD/MM/AAAA): ")
                try:
                    data_iso = converter_para_iso(data_input)
                    break
                except ValueError:
                    print("Data inválida.")

            # validar número
            while True:
                try:
                    dias = int(input("Quantidade de dias úteis: "))
                    break
                except ValueError:
                    print("Digite um número válido.")

            prazo_final = calcular_prazo(data_iso, dias)

            processos = carregar_processos()
            # verificar se já existe
            if any(p["numero"] == numero for p in processos):
                print("❌ Processo já cadastrado.")
            else:
                processos.append({
                    "numero": numero,
                    "nome": nome,
                    "prazo": prazo_final
                })
                salvar_processos(processos)
                print("✅ Processo cadastrado!")

        elif opcao == "2":
            processos = carregar_processos()

            if not processos:
                print("Nenhum processo cadastrado.")
                continue

            processos.sort(key=lambda p: datetime.strptime(p["prazo"], "%Y-%m-%d"))

            hoje = datetime.today().date()

            for p in processos:
                prazo_data = datetime.strptime(p["prazo"], "%Y-%m-%d").date()
                dias_restantes = (prazo_data - hoje).days

                prazo_br = converter_para_br(p["prazo"])

                if dias_restantes < 0:
                    status = "⚫ VENCIDO"
                elif dias_restantes <= 3:
                    status = "🔴 URGENTE"
                else:
                    status = "🟢 NORMAL"

                print("\n" + "=" * 30)
                print(f"Processo: {p['numero']}")
                print(f"Parte: {p['nome']}")
                print(f"Prazo: {prazo_br}")
                print(f"Dias restantes: {dias_restantes}")
                print(f"Status: {status}")

        elif opcao == "3":
            processos = carregar_processos()
            termo = input("Digite número ou nome: ").lower()

            encontrados = [
                p for p in processos
                if termo in p["numero"].lower() or termo in p["nome"].lower()
            ]

            if not encontrados:
                print("Nenhum processo encontrado.")
            else:
                for p in encontrados:
                    prazo_br = converter_para_br(p["prazo"])
                    print("\n" + "=" * 30)
                    print(f"Processo: {p['nome']}")
                    print(f"Prazo: {prazo_br}")

        elif opcao == "4":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()