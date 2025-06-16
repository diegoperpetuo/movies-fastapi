from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "filmes0")

logger.info(f"Conectando ao MongoDB: {MONGO_URL}")
logger.info(f"Database: {DATABASE_NAME}")

try:
    client = AsyncIOMotorClient(MONGO_URL)
    # Testar a conexão
    client.admin.command('ping')
    logger.info("Conexão com MongoDB estabelecida com sucesso!")
except Exception as e:
    logger.error(f"Erro ao conectar com MongoDB: {str(e)}")
    raise

db = client[DATABASE_NAME]
