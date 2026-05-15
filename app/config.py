from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5435/indicadores_bi"
)

WORLD_BANK_BASE_URL = os.getenv(
    "WORLD_BANK_BASE_URL",
    "https://api.worldbank.org/v2"
)

TIMEOUT_REQUISICAO = int(os.getenv("TIMEOUT_REQUISICAO", "20"))