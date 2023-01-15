from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Model(BaseModel):

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class DBModel(Model):
    id: PyObjectId = Field(alias='_id')

    class Config:
        allow_population_by_field_name = True


# Output (read) / database models
class WordlistRow(DBModel):
    phrase: str
    meaning: str
    wordlist_id: PyObjectId


class Wordlist(DBModel):
    name: str


class Dictionary(DBModel):
    name: str
    wordlists: list[PyObjectId] = []


# Input (create) models
class WordlistRowIn(Model):
    phrase: str
    meaning: str
    wordlist_id: PyObjectId


class WordlistIn(Model):
    name: str


class DictionaryIn(Model):
    name: str
    wordlists: list[PyObjectId] = []
