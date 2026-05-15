from app.database import SessionLocal
from app.etl.extract import extrair_indicador_world_bank
from app.etl.load import salvar_registros_transformados
from app.etl.transform import transformar_registros_world_bank


INDICADORES = {
    "SP.POP.TOTL": "Populacao total",
    "NY.GDP.MKTP.CD": "PIB em US$ atual",
    "NY.GDP.PCAP.CD": "PIB per capita em US$ atual",
    "SL.UEM.TOTL.ZS": "Taxa de desemprego",
}

PAISES = [
    "BRA",
    "ARG",
    "CHL",
    "URY",
    "PRY",
    "USA",
]

ANO_INICIO = 2010
ANO_FIM = 2023


def executar_pipeline_etl() -> None:
    session = SessionLocal()

    try:
        total_geral = 0

        print("=== Iniciando pipeline ETL ===")

        for codigo_indicador, nome_indicador in INDICADORES.items():
            print(f"Extraindo indicador: {codigo_indicador} - {nome_indicador}")

            registros_brutos = extrair_indicador_world_bank(
                codigo_indicador=codigo_indicador,
                codigos_paises=PAISES,
                ano_inicio=ANO_INICIO,
                ano_fim=ANO_FIM,
            )

            registros_transformados = transformar_registros_world_bank(
                registros_brutos=registros_brutos,
                codigo_indicador=codigo_indicador,
                nome_indicador=nome_indicador,
            )

            quantidade_salva = salvar_registros_transformados(
                session=session,
                registros_transformados=registros_transformados,
            )

            total_geral += quantidade_salva

            print(
                f"Indicador {codigo_indicador}: "
                f"{quantidade_salva} registros carregados/atualizados."
            )

        print("=== Pipeline ETL finalizado ===")
        print(f"Total de registros processados: {total_geral}")

    finally:
        session.close()