import logging

from dotenv import load_dotenv
from fastapi import FastAPI, status

from dictionary.db import mongo
from dictionary.db import postgres as db
from dictionary.domain import Dictionary, Wordlist, WordlistRow

load_dotenv()

logging.basicConfig(
    format='[%(asctime)s]:%(levelname)s:%(name)s:%(module)s:%(message)s',
    level=logging.INFO
)

db.initialize()
app = FastAPI()
log = logging.getLogger(__name__)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/dict')
def get_dicts() -> list[Dictionary]:
    return db.get_dicts()


@app.post('/dict', status_code=status.HTTP_201_CREATED)
def create_dict(dictionary: Dictionary):
    id_ = db.insert_dict(dictionary)
    return {'id': id_}


@app.delete('/dict/{dict_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_dict(dict_id: int):
    db.remove_dict(dict_id)


@app.get('/wordlist/{dict_id}')
def get_wordlist_by_dict_id(dict_id: int) -> list[Wordlist]:
    return db.get_wordlists(dict_id)


@app.post('/wordlist', status_code=status.HTTP_201_CREATED)
def create_wordlist(wordlist: Wordlist):
    id_ = db.insert_wordlist(wordlist)
    return {'id': id_}


@app.delete('/wordlist/{wordlist_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_wordlist(wordlist_id: int):
    db.remove_wordlist(wordlist_id)


@app.get('/wordlist-row/{wordlist_id}')
def get_wordlist_rows(wordlist_id: int) -> list[WordlistRow]:
    return db.get_wordlist_rows(wordlist_id)


@app.post('/wordlist-row', status_code=status.HTTP_201_CREATED)
def create_wordlist_row(wordlist_row: WordlistRow):
    id_ = db.insert_wordlist_row(wordlist_row)
    return {'id': id_}


@app.delete('/wordlist-row/{wordlist_row_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_wordlist_row(wordlist_row_id: int):
    db.remove_wordlist_row(wordlist_row_id)


@app.get('/mongo')
def read_dbs():
    return {'dbs': mongo.get_dbs()}