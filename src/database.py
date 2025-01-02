import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.settings import Settings
from src.models import PlanoAcaoEspecial
import logging
from tenacity import retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
async def get_engine():
    """Cria engine com tentativas de reconexão"""
    settings = Settings()
    logger.info(f"Tentando conectar ao banco de dados: {settings.DATABASE_URL}")
    
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        future=True,
        pool_pre_ping=True
    )
    
    # Testa a conexão
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)
    
    logger.info("Conexão com o banco de dados estabelecida com sucesso!")
    return engine

engine = None

async def init_db():
    global engine
    try:
        engine = await get_engine()
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")
        raise

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if engine is None:
        raise Exception("Database não foi inicializado. Chame init_db() primeiro.")
    
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session