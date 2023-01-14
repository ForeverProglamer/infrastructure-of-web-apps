import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MONGO_CONNECTION_STRING = 'mongodb://{0}:{1}@{2}'.format(
    os.getenv('MONGO_USER'),
    os.getenv('MONGO_PASSWORD'),
    os.getenv('MONGO_HOST'),
)

POSTGRES_DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT')
}
