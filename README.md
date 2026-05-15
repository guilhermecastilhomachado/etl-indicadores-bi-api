# ETL de Indicadores Econômicos + API de Consulta

## Objetivo
Projeto de portfólio desenvolvido em Python para praticar um fluxo de dados completo, envolvendo extração, transformação, carga em banco PostgreSQL e exposição dos dados por meio de uma API com FastAPI.

## Tecnologias utilizadas
- Python
- FastAPI
- PostgreSQL
- Docker Compose
- SQLAlchemy
- Requests
- Uvicorn
- python-dotenv

## Fonte de dados
O projeto utiliza dados públicos da World Bank Indicators API.

## Indicadores utilizados
- `SP.POP.TOTL` — População total
- `NY.GDP.MKTP.CD` — PIB em US$ atual
- `NY.GDP.PCAP.CD` — PIB per capita em US$ atual
- `SL.UEM.TOTL.ZS` — Taxa de desemprego

## Funcionalidades iniciais
- Extração de dados públicos via API
- Transformação dos dados para formato relacional
- Carga em PostgreSQL
- Consulta de países
- Consulta de indicadores
- Consulta de registros filtrados
- Métricas por país
- Ranking por indicador e ano
- Evolução histórica por país e indicador

## Como executar

### 1. Criar ambiente virtual
```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1