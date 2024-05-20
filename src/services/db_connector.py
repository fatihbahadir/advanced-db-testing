
import pyodbc
from pyodbc import Connection, Cursor
from threading import get_ident

from typing import Tuple

from core.app_logger import Logger

class DbConnector:

    _dbname = None
    _user = None
    _password = None
    _host = None
    _conn_str = ""

    _logger = Logger(__name__).get_logger()

    @classmethod
    def setup(cls, dbname: str, user: str, password: str, host: str) -> None:
        cls._dbname = dbname
        cls._user = user
        cls._password = password
        cls._host = host

        cls._conn_str = cls._gen_conn_str()

    @classmethod
    def connect(cls) -> Tuple[Connection, Cursor]:
        try:
            conn = pyodbc.connect(cls._conn_str)
            cursor = conn.cursor()
        except pyodbc.Error as e:
            cls._logger.error("DB connection error: " + str(e))
            raise
        cls._logger.debug(f"DB connected (thread::{get_ident()})")
        return conn, cursor

    @classmethod
    def disconnect(cls, conn_data: Tuple[Connection, Cursor]) -> None:
        conn, cursor = conn_data
        if cursor:
            cursor.close()
            cls._logger.debug(f"DB cursor closed (thread::{get_ident()})")
        if conn:
            conn.close()
            cls._logger.debug(f"DB conn closed (thread::{get_ident()})")
        cls._logger.debug(f"DB disconnected (thread::{get_ident()})")

    @classmethod
    def execute(cls, sql: str) -> any:
        conn, cursor = cls.connect()
        
        cursor.execute(sql)
        result = cursor.fetchall()
        
        cls.disconnect(conn, cursor)
        
        return result
    
    @classmethod
    def _gen_conn_str(cls):
        return f'DRIVER={{SQL Server}};SERVER={cls._host};DATABASE={cls._dbname};UID={cls._user};PWD={cls._password}'