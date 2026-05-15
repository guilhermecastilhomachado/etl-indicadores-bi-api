from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Indicador, Pais, RegistroIndicador


app = FastAPI(
    title="API de Indicadores Econômicos",
    description="API para consulta de indicadores carregados por pipeline ETL.",
    version="1.0.0",
)


def obter_sessao():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def raiz():
    return {
        "mensagem": "API de Indicadores Econômicos",
        "documentacao": "/docs",
    }


@app.get("/paises")
def listar_paises(session: Session = Depends(obter_sessao)):
    paises = session.query(Pais).order_by(Pais.nome.asc()).all()

    return [
        {
            "codigo_iso3": pais.codigo_iso3,
            "nome": pais.nome,
        }
        for pais in paises
    ]


@app.get("/indicadores")
def listar_indicadores(session: Session = Depends(obter_sessao)):
    indicadores = session.query(Indicador).order_by(Indicador.codigo.asc()).all()

    return [
        {
            "codigo": indicador.codigo,
            "nome": indicador.nome,
            "fonte": indicador.fonte,
        }
        for indicador in indicadores
    ]


@app.get("/registros")
def listar_registros(
    pais: str | None = Query(default=None, description="Codigo ISO3 do pais. Exemplo: BRA"),
    indicador: str | None = Query(default=None, description="Codigo do indicador. Exemplo: SP.POP.TOTL"),
    ano_inicio: int | None = Query(default=None),
    ano_fim: int | None = Query(default=None),
    session: Session = Depends(obter_sessao),
):
    consulta = (
        session.query(RegistroIndicador, Pais, Indicador)
        .join(Pais, RegistroIndicador.pais_id == Pais.id)
        .join(Indicador, RegistroIndicador.indicador_id == Indicador.id)
    )

    if pais:
        consulta = consulta.filter(Pais.codigo_iso3 == pais.upper())

    if indicador:
        consulta = consulta.filter(Indicador.codigo == indicador)

    if ano_inicio:
        consulta = consulta.filter(RegistroIndicador.ano >= ano_inicio)

    if ano_fim:
        consulta = consulta.filter(RegistroIndicador.ano <= ano_fim)

    resultados = (
        consulta
        .order_by(Pais.codigo_iso3.asc(), Indicador.codigo.asc(), RegistroIndicador.ano.asc())
        .all()
    )

    return [
        {
            "pais": pais_obj.codigo_iso3,
            "nome_pais": pais_obj.nome,
            "indicador": indicador_obj.codigo,
            "nome_indicador": indicador_obj.nome,
            "ano": registro.ano,
            "valor": float(registro.valor),
        }
        for registro, pais_obj, indicador_obj in resultados
    ]


@app.get("/metricas/resumo/{codigo_pais}")
def resumo_por_pais(
    codigo_pais: str,
    session: Session = Depends(obter_sessao),
):
    pais = session.query(Pais).filter_by(codigo_iso3=codigo_pais.upper()).first()

    if not pais:
        raise HTTPException(status_code=404, detail="Pais nao encontrado.")

    registros = (
        session.query(RegistroIndicador, Indicador)
        .join(Indicador, RegistroIndicador.indicador_id == Indicador.id)
        .filter(RegistroIndicador.pais_id == pais.id)
        .order_by(Indicador.codigo.asc(), desc(RegistroIndicador.ano))
        .all()
    )

    resumo = {}

    for registro, indicador in registros:
        if indicador.codigo not in resumo:
            resumo[indicador.codigo] = {
                "indicador": indicador.codigo,
                "nome_indicador": indicador.nome,
                "ano_mais_recente": registro.ano,
                "valor": float(registro.valor),
            }

    return {
        "pais": pais.codigo_iso3,
        "nome_pais": pais.nome,
        "indicadores": list(resumo.values()),
    }


@app.get("/metricas/ranking")
def ranking_por_indicador(
    indicador: str = Query(..., description="Codigo do indicador. Exemplo: NY.GDP.MKTP.CD"),
    ano: int = Query(..., description="Ano de referencia. Exemplo: 2023"),
    limite: int = Query(default=10, ge=1, le=50),
    session: Session = Depends(obter_sessao),
):
    indicador_obj = session.query(Indicador).filter_by(codigo=indicador).first()

    if not indicador_obj:
        raise HTTPException(status_code=404, detail="Indicador nao encontrado.")

    registros = (
        session.query(RegistroIndicador, Pais)
        .join(Pais, RegistroIndicador.pais_id == Pais.id)
        .filter(
            RegistroIndicador.indicador_id == indicador_obj.id,
            RegistroIndicador.ano == ano,
        )
        .order_by(desc(RegistroIndicador.valor))
        .limit(limite)
        .all()
    )

    return {
        "indicador": indicador_obj.codigo,
        "nome_indicador": indicador_obj.nome,
        "ano": ano,
        "ranking": [
            {
                "posicao": indice + 1,
                "pais": pais.codigo_iso3,
                "nome_pais": pais.nome,
                "valor": float(registro.valor),
            }
            for indice, (registro, pais) in enumerate(registros)
        ],
    }


@app.get("/metricas/evolucao")
def evolucao_indicador(
    pais: str = Query(..., description="Codigo ISO3 do pais. Exemplo: BRA"),
    indicador: str = Query(..., description="Codigo do indicador. Exemplo: NY.GDP.PCAP.CD"),
    session: Session = Depends(obter_sessao),
):
    pais_obj = session.query(Pais).filter_by(codigo_iso3=pais.upper()).first()

    if not pais_obj:
        raise HTTPException(status_code=404, detail="Pais nao encontrado.")

    indicador_obj = session.query(Indicador).filter_by(codigo=indicador).first()

    if not indicador_obj:
        raise HTTPException(status_code=404, detail="Indicador nao encontrado.")

    registros = (
        session.query(RegistroIndicador)
        .filter_by(
            pais_id=pais_obj.id,
            indicador_id=indicador_obj.id,
        )
        .order_by(RegistroIndicador.ano.asc())
        .all()
    )

    return {
        "pais": pais_obj.codigo_iso3,
        "nome_pais": pais_obj.nome,
        "indicador": indicador_obj.codigo,
        "nome_indicador": indicador_obj.nome,
        "serie": [
            {
                "ano": registro.ano,
                "valor": float(registro.valor),
            }
            for registro in registros
        ],
    }