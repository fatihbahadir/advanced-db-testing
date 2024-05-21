
import pyodbc
from pyodbc import Connection, Cursor
from threading import get_ident

from typing import Tuple

from core.app_logger import Logger
from modules.worker.enums import TransactionIsolationLevel

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
    def create_index(cls):
        try:
            sql = """CREATE INDEX idx_UnitPrice ON Sales.SalesOrderDetail(UnitPrice);
                    CREATE INDEX idx_SalesOrderID ON Sales.SalesOrderDetail(SalesOrderID);
                    CREATE INDEX idx_OrderDate ON Sales.SalesOrderHeader(OrderDate);
                    CREATE INDEX idx_OnlineOrderFlag ON Sales.SalesOrderHeader(OnlineOrderFlag)"""
            conn, cursor = cls.connect()
            cursor.execute(sql)
            conn.commit()

            indexes = [
                'idx_UnitPrice',
                'idx_SalesOrderID',
                'idx_OrderDate',
                'idx_OnlineOrderFlag'
            ]

            for index in indexes:
                cursor.execute(f"SELECT name FROM sys.indexes WHERE name = '{index}'")
                result = cursor.fetchone()
                if result:
                    cls._logger.info(f"Index {index} created successfully.")
                else:
                    cls._logger.warn(f"Index {index} was not created.")

            cls.disconnect((conn, cursor))
        except Exception as e:
            cls._logger.warn(f"Index # UEO on create Index: {e}")

    @classmethod
    def drop_index(cls):
        try:
            sql = """DROP INDEX idx_UnitPrice ON Sales.SalesOrderDetail;
                    DROP INDEX idx_SalesOrderID ON Sales.SalesOrderDetail;
                    DROP INDEX idx_OrderDate ON Sales.SalesOrderHeader;
                    DROP INDEX idx_OnlineOrderFlag ON Sales.SalesOrderHeader;"""

            conn, cursor = cls.connect()
            cursor.execute(sql)
            conn.commit()

            # Verify the indexes were dropped
            indexes = [
                'idx_UnitPrice',
                'idx_SalesOrderID',
                'idx_OrderDate',
                'idx_OnlineOrderFlag'
            ]

            for index in indexes:
                cursor.execute(f"SELECT name FROM sys.indexes WHERE name = '{index}'")
                result = cursor.fetchone()
                if not result:
                    cls._logger.info(f"Index {index} dropped successfully.")
                else:
                    cls._logger.warn(f"Index {index} was not dropped.")

            cls.disconnect((conn, cursor))
        except Exception as e:
            cls._logger.warn(f"Index # UEO on drop Index: {e}")


    @classmethod
    def set_isolation_level(cls, cursor: Cursor, isolation_level: TransactionIsolationLevel):
        if isinstance(isolation_level, TransactionIsolationLevel):
            level_name = isolation_level.value.upper()
            try:
                cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {level_name}")
                # Verify the isolation level was set
                cursor.execute("DBCC USEROPTIONS")
                options = cursor.fetchall()
                isolation_level_set = False
                for option in options:
                    if option[0] == 'isolation level':
                        if option[1].upper() == level_name:
                            isolation_level_set = True
                            cls._logger.info(f"Transaction isolation level set to {level_name}")
                        break
                if not isolation_level_set:
                    cls._logger.warn(f"Failed to set transaction isolation level to {level_name}")
            except Exception as e:
                cls._logger.error(f"Error setting transaction isolation level: {e}")
                raise
        else:
            cls._logger.error("Invalid isolation level")


    @classmethod
    def commit_isolation(cls, cursor: Cursor):
        cursor.connection.commit()

    @classmethod
    def rollback(cls, cursor: Cursor):
        cursor.connection.rollback()

    @classmethod
    def begin_transaction(cls, cursor: Cursor):
        cursor.execute("BEGIN TRANSACTION")
       
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