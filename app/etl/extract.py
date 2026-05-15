import requests

from app.config import TIMEOUT_REQUISICAO, WORLD_BANK_BASE_URL


def extrair_indicador_world_bank(
    codigo_indicador: str,
    codigos_paises: list[str],
    ano_inicio: int,
    ano_fim: int,
) -> list[dict]:
    paises_parametro = ";".join(codigos_paises)

    url = (
        f"{WORLD_BANK_BASE_URL}/country/{paises_parametro}"
        f"/indicator/{codigo_indicador}"
    )

    parametros = {
        "format": "json",
        "per_page": 20000,
        "date": f"{ano_inicio}:{ano_fim}",
    }

    resposta = requests.get(url, params=parametros, timeout=TIMEOUT_REQUISICAO)
    resposta.raise_for_status()

    dados = resposta.json()

    if not isinstance(dados, list) or len(dados) < 2:
        return []

    registros = dados[1]

    if registros is None:
        return []

    return registros