import os
from typing import Callable, TypeVar, Optional
from logging import getLogger
from functools import wraps

from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from psycopg2.errors import Error

from dictionary.schemas.postgres import Dictionary, Wordlist, WordlistRow
from dictionary.config import POSTGRES_DB_CONFIG

log = getLogger(__name__)

CREATE_DB_SQL = f"""CREATE DATABASE {os.getenv('DB_NAME')}""" 

CREATE_DICTS_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS dicts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(30) NOT NULL UNIQUE
    )
"""

CREATE_FOLDER_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS wordlists (
        id SERIAL PRIMARY KEY,
        name VARCHAR(30) NOT NULL UNIQUE,
        dict_id INT NOT NULL,
        CONSTRAINT fk_dicts FOREIGN KEY(dict_id) REFERENCES dicts(id) ON DELETE CASCADE
    )
"""

CREATE_WORDLIST_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS wordlist_rows (
        id SERIAL PRIMARY KEY,
        phrase TEXT NOT NULL,
        meaning TEXT NOT NULL,
        wordlist_id INT NOT NULL,
        CONSTRAINT fk_wordlists FOREIGN KEY(wordlist_id) REFERENCES wordlists(id) ON DELETE CASCADE,
        UNIQUE(phrase, meaning, wordlist_id)
    )
"""

INSERT_DICT_SQL = """
    INSERT INTO dicts (name) VALUES (%s) RETURNING id
"""

INSERT_WORDLIST_SQL = """
    INSERT INTO wordlists (name, dict_id) VALUES (%s, %s) RETURNING id
"""

INSERT_WORDLIST_ROW_SQL = """
    INSERT INTO wordlist_rows (phrase, meaning, wordlist_id) VALUES (%s, %s, %s) RETURNING id
"""

SELECT_ALL_DICTS_SQL = """
    SELECT * FROM dicts
"""

SELECT_DICT_WORDLISTS_SQL = """
    SELECT * FROM wordlists WHERE dict_id = %s
"""

SELECT_WORDLIST_ROWS_SQL = """
    SELECT * FROM wordlist_rows WHERE wordlist_id = %s
"""

DELETE_DICT_SQL = """
    DELETE FROM dicts WHERE id = %s
"""

DELETE_WORDLIST_SQL = """
    DELETE FROM wordlists WHERE id = %s
"""

DELETE_WORDLIST_ROW_SQL = """
    DELETE FROM wordlist_rows WHERE id = %s
"""

T = TypeVar('T')


def pg_connection(autocommit: bool = False) -> Callable[..., Callable[..., T]]:
    def fn_wrapper(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        def args_wrapper(*args, **kwargs) -> T:
            try:
                conn = connect(**POSTGRES_DB_CONFIG)
                conn.autocommit = autocommit
                res = fn(conn, *args, **kwargs)
            except Error as e:
                log.exception(e)
                if not autocommit:
                    conn.rollback()
                raise e
            else:
                if not autocommit:
                    conn.commit()
            finally:
                conn.close()
            return res
        return args_wrapper
    return fn_wrapper


def initialize() -> None:
    _create_db()
    _create_tables()


@pg_connection(autocommit=True)
def _create_db(conn: connection) -> None:
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_DB_SQL)
    except Error as e:
        log.exception(e)
    finally:
        POSTGRES_DB_CONFIG['database'] = os.getenv('DB_NAME')


@pg_connection()
def _create_tables(conn: connection) -> None:
    try:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_DICTS_TABLE_SQL)
            cursor.execute(CREATE_FOLDER_TABLE_SQL)
            cursor.execute(CREATE_WORDLIST_TABLE_SQL)
    except Error as e:
        log.exception(e)


@pg_connection()
def insert_dict(conn: connection, dict_: Dictionary) -> Optional[int]:
    try:
        with conn.cursor() as cur:
            cur.execute(INSERT_DICT_SQL, (dict_.name,))
            return cur.fetchone()[0]
    except Error as e:
        log.exception(e)
        return None


@pg_connection()
def insert_wordlist(
    conn: connection,
    wordlist: Wordlist
) -> Optional[int]:
    try:
        with conn.cursor() as cur:
            cur.execute(
                INSERT_WORDLIST_SQL, (wordlist.name, wordlist.dict_id)
            )
            return cur.fetchone()[0]
    except Error as e:
        log.exception(e)
        return None


@pg_connection()
def insert_wordlist_row(
    conn: connection,
    wordlist_row: WordlistRow
) -> Optional[int]:
    try:
        with conn.cursor() as cur:
            cur.execute(
                INSERT_WORDLIST_ROW_SQL,
                (
                    wordlist_row.phrase,
                    wordlist_row.meaning,
                    wordlist_row.wordlist_id
                )
            )
            return cur.fetchone()[0]
    except Error as e:
        log.exception(e)
        return None


@pg_connection()
def get_dicts(conn: connection) -> list[Dictionary]:
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(SELECT_ALL_DICTS_SQL)
            return [Dictionary.parse_obj(row) for row in cur]
    except Error as e:
        log.exception(e)
        return []


@pg_connection()
def get_wordlists(conn: connection, dict_id: int) -> list[Wordlist]:
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(SELECT_DICT_WORDLISTS_SQL, (dict_id,))
            return [Wordlist.parse_obj(row) for row in cur]
    except Error as e:
        log.exception(e)
        return []


@pg_connection()
def get_wordlist_rows(
    conn: connection,
    wordlist_id: int
) -> list[WordlistRow]:
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(SELECT_WORDLIST_ROWS_SQL, (wordlist_id,))
            return [WordlistRow.parse_obj(row) for row in cur]
    except Error as e:
        log.exception(e)
        return []


@pg_connection()
def remove_dict(conn: connection, dict_id: int) -> bool:
    try:
        with conn.cursor() as cur:
            cur.execute(DELETE_DICT_SQL, (dict_id,))
            return cur.rowcount > 0
    except Error as e:
        log.exception(e)
        return False


@pg_connection()
def remove_wordlist(conn: connection, wordlist_id: int) -> bool:
    try:
        with conn.cursor() as cur:
            cur.execute(DELETE_WORDLIST_SQL, (wordlist_id,))
            return cur.rowcount > 0
    except Error as e:
        log.exception(e)
        return False


@pg_connection()
def remove_wordlist_row(conn: connection, wordlist_row_id: int) -> bool:
    try:
        with conn.cursor() as cur:
            cur.execute(DELETE_WORDLIST_ROW_SQL, (wordlist_row_id,))
            return cur.rowcount > 0
    except Error as e:
        log.exception(e)
        return False
