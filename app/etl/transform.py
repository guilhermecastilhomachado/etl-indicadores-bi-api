from decimal import Decimal, InvalidOperation


def converter_valor_para_decimal(valor) -> Decimal | None:
    if valor is None:
        return None

    try:
        return Decimal(str(valor)).quantize(Decimal("0.01"))
    except InvalidOperation:
        return None


def transformar_registros_world_bank(
    registros_brutos: list[dict],
    codigo_indicador: str,
    nome_indicador: str,
    fonte: str = "World Bank",
) -> list[dict]:
    registros_transformados = []

    for item in registros_brutos:
        valor = converter_valor_para_decimal(item.get("value"))

        if valor is None:
            continue

        codigo_pais = item.get("countryiso3code")
        nome_pais = item.get("country", {}).get("value")
        ano_texto = item.get("date")

        if not codigo_pais or not nome_pais or not ano_texto:
            continue

        try:
            ano = int(ano_texto)
        except ValueError:
            continue

        registros_transformados.append(
            {
                "codigo_pais": codigo_pais,
                "nome_pais": nome_pais,
                "codigo_indicador": codigo_indicador,
                "nome_indicador": nome_indicador,
                "fonte": fonte,
                "ano": ano,
                "valor": valor,
            }
        )

    return registros_transformados