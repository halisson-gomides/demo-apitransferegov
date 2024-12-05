from http import HTTPStatus
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.schemas import Message
from src.database import get_session, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load before the app starts
    await init_db()
    yield
    # load after the app has finished
    # ...

app = FastAPI(lifespan=lifespan)

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}