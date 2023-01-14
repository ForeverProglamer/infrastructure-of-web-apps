from typing import Optional

from pydantic import BaseModel


class Entity(BaseModel):
    id: Optional[int] = None


class Dictionary(Entity):
    name: str


class Wordlist(Entity):
    name: str
    dict_id: int


class WordlistRow(Entity):
    phrase: str
    meaning: str
    wordlist_id: int