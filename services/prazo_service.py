from datetime import datetime, timedelta


def calcular_prazo(data_inicial, dias_uteis):
    data = datetime.strptime(data_inicial, "%Y-%m-%d")

    dias_contados = 0

    while dias_contados < dias_uteis:
        data += timedelta(days=1)

        if data.weekday() < 5:  # segunda a sexta
            dias_contados += 1

    return data.strftime("%Y-%m-%d")