from logging import getLogger

from fastapi import APIRouter, Request, status

from dictionary.schemas.postgres import Dictionary, Wordlist, WordlistRow

log = getLogger(__name__)

router = APIRouter()


@router.get('/dict')
def get_dicts(request: Request) -> list[Dictionary]:
    return request.app.postgres.get_dicts()


@router.post('/dict', status_code=status.HTTP_201_CREATED)
def create_dict(dictionary: Dictionary, request: Request):
    id_ = request.app.postgres.insert_dict(dictionary)
    return {'id': id_}


@router.delete('/dict/{dict_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_dict(dict_id: int, request: Request):
    request.app.postgres.remove_dict(dict_id)


@router.get('/wordlist/{dict_id}')
def get_wordlist_by_dict_id(dict_id: int, request: Request) -> list[Wordlist]:
    return request.app.postgres.get_wordlists(dict_id)


@router.post('/wordlist', status_code=status.HTTP_201_CREATED)
def create_wordlist(wordlist: Wordlist, request: Request):
    id_ = request.app.postgres.insert_wordlist(wordlist)
    return {'id': id_}


@router.delete('/wordlist/{wordlist_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_wordlist(wordlist_id: int, request: Request):
    request.app.postgres.remove_wordlist(wordlist_id)


@router.get('/wordlist-row/{wordlist_id}')
def get_wordlist_rows(wordlist_id: int, request: Request) -> list[WordlistRow]:
    return request.app.postgres.get_wordlist_rows(wordlist_id)


@router.post('/wordlist-row', status_code=status.HTTP_201_CREATED)
def create_wordlist_row(wordlist_row: WordlistRow, request: Request):
    id_ = request.app.postgres.insert_wordlist_row(wordlist_row)
    return {'id': id_}


@router.delete('/wordlist-row/{wordlist_row_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_wordlist_row(wordlist_row_id: int, request: Request):
    request.app.postgres.remove_wordlist_row(wordlist_row_id)
