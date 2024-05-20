
import psycopg2
from psycopg2.sql import SQL
from psycopg2.extensions import connection, cursor
from threading import get_ident

from typing import Tuple

from core.app_logger import Logger

class DbConnector:

    _dbname = None
    _user = None
    _password = None
    _host = None
    _port = None

    _logger = Logger(__name__).get_logger()

    @classmethod
    def setup(cls, dbname: str, user: str, password: str, host: str, port: str) -> None:
        cls._dbname = dbname
        cls._user = user
        cls._password = password
        cls._host = host
        cls._port = port

    @classmethod
    def connect(cls) -> Tuple[connection, cursor]:
        try:
            conn = psycopg2.connect(
                dbname=cls._dbname,
                user=cls._user,
                password=cls._password,
                host=cls._host,
                port=cls._port
            )
            cursor = conn.cursor()
        except psycopg2.Error as e:
            cls._logger.error("DB connection error: " + str(e))
            raise
        cls._logger.debug(f"DB connected (thread::{get_ident()})")
        return conn, cursor

    @classmethod
    def disconnect(cls, conn_data: Tuple[connection, cursor]) -> None:
        conn, cursor = conn_data
        if cursor:
            cursor.close()
            cls._logger.debug(f"DB cursor closed (thread::{get_ident()})")
        if conn:
            conn.close()
            cls._logger.debug(f"DB conn closed (thread::{get_ident()})")
        cls._logger.debug(f"DB disconnected (thread::{get_ident()})")

    @classmethod
    def execute(cls, sql: SQL) -> any:
        conn, cursor = cls.connect()
        
        cursor.execute(sql)
        result = cursor.fetchall()
        
        cls.disconnect(conn, cursor)
        
        return result