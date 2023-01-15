from logging import getLogger

from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder

from dictionary.schemas.mongo import (
    Dictionary,
    PyObjectId,
    Wordlist,
    WordlistRow,
    DictionaryIn,
    WordlistIn,
    WordlistRowIn
)

log = getLogger(__name__)

router = APIRouter()


@router.get('/dict')
def get_dicts(request: Request) -> list[Dictionary]:
    return [Dictionary(**d) for d in request.app.mongo_db.dicts.find()]


@router.post('/dict', status_code=status.HTTP_201_CREATED)
def create_dict(dictionary: DictionaryIn, request: Request):
    dict_ = jsonable_encoder(dictionary)
    id_ = request.app.mongo_db.dicts.insert_one(dict_).inserted_id
    return {'_id': str(id_)}


@router.delete('/dict/{dict_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_dict(dict_id: PyObjectId, request: Request):
    wordlist_ids = request.app.mongo_db.dicts.find_one(
        {'_id': dict_id}, {'wordlists': 1, '_id': 0}
    ).get('wordlists')
    request.app.mongo_db.wordlist_rows.delete_many(
        {'wordlist_id': {'$in': wordlist_ids}}
    )
    request.app.mongo_db.wordlists.delete_many(
        {'_id': {'$in': wordlist_ids}}
    )
    request.app.mongo_db.dicts.delete_one({'_id': dict_id})


@router.get('/dict/{dict_id}/wordlist')
def get_wordlists_by_dict_id(dict_id: PyObjectId, request: Request) -> list[Wordlist]:
    wordlist_ids = request.app.mongo_db.dicts.find_one(
        {'_id': dict_id}, {'wordlists': 1, '_id': 0}
    ).get('wordlists')
    return [Wordlist(**w) for w in request.app.mongo_db.wordlists.find(
        {'_id': {'$in': wordlist_ids}}
    )]


@router.post('/dict/{dict_id}/wordlist', status_code=status.HTTP_201_CREATED)
def create_wordlist(dict_id: PyObjectId, wordlist: WordlistIn, request: Request):
    wordlist_data = jsonable_encoder(wordlist)
    id_ = request.app.mongo_db.wordlists.insert_one(wordlist_data).inserted_id
    request.app.mongo_db.dicts.update_one(
        {'_id': dict_id}, {'$addToSet': {'wordlists': id_}}
    )
    return {'_id': str(id_)}


@router.delete('/dict/wordlist/{wordlist_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_wordlist(wordlist_id: PyObjectId, request: Request):
    request.app.mongo_db.dicts.update_one(
        {'wordlists': wordlist_id}, {'$pull': {'wordlists': wordlist_id}}
    )
    request.app.mongo_db.wordlist_rows.delete_many({'wordlist_id': wordlist_id})
    request.app.mongo_db.wordlists.delete_one({'_id': wordlist_id})


@router.get('/wordlist/{wordlist_id}/row')
def get_wordlist_rows(wordlist_id: PyObjectId, request: Request) -> list[WordlistRow]:
    return [WordlistRow(**w) for w in request.app.mongo_db.wordlist_rows.find(
        {'wordlist_id': wordlist_id}
    )]


@router.post('/wordlist/row', status_code=status.HTTP_201_CREATED)
def create_wordlist_row(wordlist_row: WordlistRowIn, request: Request):
    data = wordlist_row.dict()
    id_ = request.app.mongo_db.wordlist_rows.insert_one(data).inserted_id
    return {'_id': str(id_)}


@router.delete('/wordlist/row/{wordlist_row_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_wordlist_row(wordlist_row_id: PyObjectId, request: Request):
    request.app.mongo_db.wordlist_rows.delete_one({'_id': wordlist_row_id})