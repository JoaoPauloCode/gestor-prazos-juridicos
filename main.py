from utils import carregar_processos, salvar_processos, converter_para_iso, converter_para_br, calcular_prioridade

def menu():
    print("\n--- Organizador de Processos ---")
    print("1 - Cadastrar processo")
    print("2 - Listar processos")
    print("3 - Buscar processo")
    print("4 - Sair")


while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome do Autor(a): ")
        while True:
            prazo_input = input("Prazo (DD/MM/AAAA): ")
            try:
                prazo = converter_para_iso(prazo_input)
                break
            except:
                print("Data inválida. Tente novamente.")


        processos = carregar_processos()

        prioridade = calcular_prioridade(prazo)

        processos.append({
            "nome": nome,
            "prazo": prazo,
            "prioridade": prioridade
        })

        salvar_processos(processos)

        print("Processo cadastrado com sucesso!")

    elif opcao == "2":
        from datetime import datetime
        
        hoje = datetime.now().date()
        processos = carregar_processos()

        for p in processos:
            prazo_data = datetime.strptime(p["prazo"], "%Y-%m-%d").date()
            dias_restantes = (prazo_data - hoje).days

            prazo_br = converter_para_br(p["prazo"])

            if dias_restantes <= 3:
                status = "🔴 URGENTE"
            elif dias_restantes <= 7:
                status = "🟡 Normal"
            else:
                status = "🟢 Baixa"

            print(f"Nome: {p['nome']}")
            print(f"Prazo: {prazo_br}")
            print(f"Status: {status}")
            print("-" * 20)

    elif opcao == "3":
        termo = input("Digite o nome para buscar: ").lower()

        processos = carregar_processos()

        encontrados = [p for p in processos if termo in p["nome"].lower()]

        if not encontrados:
            print("Nenhum processo encontrado.")
        else:
            for p in encontrados:
                prazo_br = converter_para_br(p["prazo"])
                prioridade = calcular_prioridade(p["prazo"])  # Recalcula prioridade atual
                print(f"Nome: {p['nome']}")
                print(f"Prazo: {prazo_br}")
                print(f"Prioridade: {prioridade}")
                print("-" * 20)
    
    elif opcao == "4":
        print("Saindo...")
        break

    else:
        print("Opção inválida")