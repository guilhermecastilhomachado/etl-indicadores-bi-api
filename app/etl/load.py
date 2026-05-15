from sqlalchemy.orm import Session

from app.models import Indicador, Pais, RegistroIndicador


def obter_ou_criar_pais(session: Session, codigo_iso3: str, nome: str) -> Pais:
    pais = session.query(Pais).filter_by(codigo_iso3=codigo_iso3).first()

    if pais:
        if pais.nome != nome:
            pais.nome = nome
        return pais

    pais = Pais(codigo_iso3=codigo_iso3, nome=nome)
    session.add(pais)
    session.flush()

    return pais


def obter_ou_criar_indicador(
    session: Session,
    codigo: str,
    nome: str,
    fonte: str,
) -> Indicador:
    indicador = session.query(Indicador).filter_by(codigo=codigo).first()

    if indicador:
        indicador.nome = nome
        indicador.fonte = fonte
        return indicador

    indicador = Indicador(
        codigo=codigo,
        nome=nome,
        fonte=fonte,
    )
    session.add(indicador)
    session.flush()

    return indicador


def salvar_registros_transformados(
    session: Session,
    registros_transformados: list[dict],
) -> int:
    quantidade_salva = 0

    for registro in registros_transformados:
        pais = obter_ou_criar_pais(
            session=session,
            codigo_iso3=registro["codigo_pais"],
            nome=registro["nome_pais"],
        )

        indicador = obter_ou_criar_indicador(
            session=session,
            codigo=registro["codigo_indicador"],
            nome=registro["nome_indicador"],
            fonte=registro["fonte"],
        )

        registro_existente = (
            session.query(RegistroIndicador)
            .filter_by(
                pais_id=pais.id,
                indicador_id=indicador.id,
                ano=registro["ano"],
            )
            .first()
        )

        if registro_existente:
            registro_existente.valor = registro["valor"]
        else:
            novo_registro = RegistroIndicador(
                pais_id=pais.id,
                indicador_id=indicador.id,
                ano=registro["ano"],
                valor=registro["valor"],
            )
            session.add(novo_registro)

        quantidade_salva += 1

    session.commit()
    return quantidade_salva