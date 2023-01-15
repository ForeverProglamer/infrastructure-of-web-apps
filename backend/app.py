import logging

from fastapi import FastAPI
from pymongo import MongoClient

from dictionary import postgres
from dictionary.config import MONGO_CONNECTION_STRING
from dictionary.routes.postgres import router as postgres_router
from dictionary.routes.mongo import router as mongo_router

logging.basicConfig(
    format='[%(asctime)s]:%(levelname)s:%(name)s:%(module)s:%(message)s',
    level=logging.INFO
)

app = FastAPI()
log = logging.getLogger(__name__)


@app.on_event('startup')
def startup():
    postgres.initialize()
    app.postgres = postgres
    app.mongo_client = MongoClient(MONGO_CONNECTION_STRING)
    app.mongo_db = app.mongo_client.dict_app
    log.info('Postgres and MongoDB are successfully initialized')


@app.on_event('shutdown')
def shutdown():
    app.mongo_client.close()
    log.info('MongoDB is successfully closed')


app.include_router(postgres_router, prefix='/pg')
app.include_router(mongo_router, prefix='/mongo')