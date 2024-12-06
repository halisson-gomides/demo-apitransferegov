from http import HTTPStatus
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from src.schemas import Message
from src.database import get_session, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load before the app starts
    logger.info("Iniciando aplicação...")
    try:
        await init_db()
        logger.info("Banco de dados inicializado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
        raise
    yield
    # load after the app has finished
    # ...

app = FastAPI(lifespan=lifespan)

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}