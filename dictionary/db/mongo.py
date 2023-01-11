import os

import pymongo


CONNECTION_STRING = 'mongodb://{0}:{1}@{2}'.format(
    os.getenv('MONGO_USER'),
    os.getenv('MONGO_PASSWORD'),
    os.getenv('MONGO_HOST'),
)

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.dictionary


def get_dbs() -> list[str]:
    return client.list_database_names()