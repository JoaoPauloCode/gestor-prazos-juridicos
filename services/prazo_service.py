from datetime import datetime, timedelta

FERIADOS = {
    "2026-01-01","2026-02-16","2026-02-17","2026-02-18",
    "2026-04-03","2026-04-05","2026-04-21","2026-05-01",
    "2026-06-04","2026-09-07","2026-10-12","2026-11-02",
    "2026-11-15","2026-11-20","2026-12-25"
}


def eh_dia_util(data):
    data_str = data.strftime("%Y-%m-%d")
    return data.weekday() < 5 and data_str not in FERIADOS


def proximo_dia_util(data):
    while not eh_dia_util(data):
        data += timedelta(days=1)
    return data


def calcular_prazo(data_inicial, dias_uteis):
    data = datetime.strptime(data_inicial, "%Y-%m-%d")

    # começa no próximo dia útil
    data = proximo_dia_util(data + timedelta(days=1))

    dias_contados = 0

    while dias_contados < dias_uteis:
        if eh_dia_util(data):
            dias_contados += 1

        if dias_contados < dias_uteis:
            data += timedelta(days=1)

    return data.strftime("%Y-%m-%d")