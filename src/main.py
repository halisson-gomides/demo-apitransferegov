from http import HTTPStatus
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
import logging
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from src.schemas import DefaultMessage
from src.database import get_session, init_db

# Rotas
from src.routers.plano_acao import pda_router

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


app = FastAPI(lifespan=lifespan, docs_url=None, title="API TranfereGov", description="Demonstração")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Router principal
router = APIRouter()

@router.get('/', 
         status_code=HTTPStatus.OK, 
         response_model=DefaultMessage,
         description="Demonstração de funcionamento")
async def read_test():
    return DefaultMessage(message="Teste API Transferegov")
    

# Incluindo os routers
app.include_router(router, prefix='/teste')
app.include_router(pda_router)


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API TransfereGov",        
        swagger_favicon_url="/static/icon.jpg"
    )


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')