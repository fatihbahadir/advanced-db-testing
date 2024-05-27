import pyodbc
from pyodbc import Cursor
from threading import get_ident
from random import random
import time
from modules.worker.enums import TransactionIsolationLevel

from modules.worker.base_worker import WorkerManager
from services.db_connector import DbConnector

class AWorkerManager(WorkerManager):

    def __init__(self, 
                 worker_amount: int, 
                 increment_complete: callable,
                 increment_deadlock: callable,
                 set_average: callable,
                 isolation_level: TransactionIsolationLevel) -> None:
        super().__init__(worker_amount, increment_complete, increment_deadlock, set_average, isolation_level)

        self.job_query = """UPDATE Sales.SalesOrderDetail
                            SET UnitPrice = UnitPrice * 10.0 / 10.0
                            WHERE UnitPrice > 100
                            AND EXISTS (SELECT * FROM Sales.SalesOrderHeader
                            WHERE Sales.SalesOrderHeader.SalesOrderID =
                            Sales.SalesOrderDetail.SalesOrderID
                            AND Sales.SalesOrderHeader.OrderDate
                            BETWEEN ? AND ?
                            AND Sales.SalesOrderHeader.OnlineOrderFlag = 1)"""
    
    def job(self):
        _start_time = time.time()
        for index in range(100):

            print(f"A-Worker Thread({get_ident()}) ~ Job :: {index + 1}")

            conn, cursor = DbConnector.connect()
            DbConnector.set_isolation_level(cursor, self.isolation_level)
            DbConnector.begin_transaction(cursor)
            try:
                self._random_execute(cursor)
                DbConnector.commit_isolation(cursor)
            except pyodbc.Error as e:
                self._logger.debug("DB error [worker#a]: " + str(e))
                if e.args[0] == 40001 or "deadlock" in e.args[1].lower():
                    self._logger.warn(f"DB deadlock [worker#a] (thread::{get_ident()}) [{self.__class__.__name__}]")
                    
                    self.number_of_deadlocks += 1
                    self.increment_deadlock()
                    DbConnector.rollback(cursor)
            except Exception as e:
                print(f"Anything ~ (thread:{get_ident()}) [{self.__class__.__name__}]")
                DbConnector.rollback(cursor)
            finally:
                DbConnector.disconnect(conn_data=(conn, cursor))
        _end_time = time.time()
        _elapsed_time = _end_time - _start_time
        print(f"Thread[A-Worker] ({get_ident()}) : {_elapsed_time}")
        self.total_elapsed_time_per_worker += _elapsed_time
        self._update_ui()

    def _random_execute(self, cursor: Cursor):
        if random() < 0.5:
            print(f"Thread({get_ident()})#A-Worker 1. random")
            cursor.execute(self.job_query, ("20110101", "20111231"))
        if random() < 0.5:
            print(f"Thread({get_ident()})#A-Worker 2. random")
            cursor.execute(self.job_query, ("20120101", "20121231"))
        if random() < 0.5:
            print(f"Thread({get_ident()})#A-Worker 3. random")
            cursor.execute(self.job_query, ("20130101", "20131231"))
        if random() < 0.5:
            print(f"Thread({get_ident()})#A-Worker 4. random")
            cursor.execute(self.job_query, ("20140101", "20141231"))
        if random() < 0.5:
            print(f"Thread({get_ident()})#A-Worker 5. random")
            cursor.execute(self.job_query, ("20150101", "20151231"))