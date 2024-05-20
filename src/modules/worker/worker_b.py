
import pyodbc
from pyodbc import Cursor
from threading import get_ident, Event
from random import random
import time

from modules.worker.base_worker import WorkerManager
from services.db_connector import DbConnector

class BWorkerManager(WorkerManager):

    def __init__(self, 
                 worker_amount: int,
                 increment_complete: callable,
                 increment_deadlock: callable,
                 set_average: callable) -> None:
        super().__init__(worker_amount, increment_complete, increment_deadlock, set_average)

        self.job_query = """SELECT SUM(Sales.SalesOrderDetail.OrderQty)
                                FROM Sales.SalesOrderDetail
                                WHERE UnitPrice > 100
                                AND EXISTS (SELECT * FROM Sales.SalesOrderHeader
                                WHERE Sales.SalesOrderHeader.SalesOrderID =
                                Sales.SalesOrderDetail.SalesOrderID
                                AND Sales.SalesOrderHeader.OrderDate
                                BETWEEN @BeginDate AND @EndDate
                                AND Sales.SalesOrderHeader.OnlineOrderFlag = 1)"""

    def job(self):

        _start_time = time.time()

        for _ in range(100):

            conn, cursor = DbConnector.connect()

            try:
                self._random_execute(cursor)
                print(f"Exec res ~ (thread:{get_ident()}) [{self.__class__.__name__}]")
            except pyodbc.Error as e:
                self._logger.debug("DB error [worker#b]: " + str(e))
                if e.args[0] == 40001 or "deadlock" in e.args[1].lower():
                    print("Deadlock ~")
                    print(f"Deadlock ~ (thread:{get_ident()})")
                    self._logger.warn(f"DB deadlock [worker#b] (thread::{get_ident()})")
                    
                    self._deadlock_occured()
            except Exception as e:
                print(f"Anything ~ (thread:{get_ident()}) [{self.__class__.__name__}]")

            DbConnector.disconnect(conn_data=(conn, cursor))

        _end_time = time.time()
        self.total_elapsed_time_per_worker += _end_time - _start_time
        
        self._update_ui()

    def _random_execute(self, cursor: Cursor):

        if random() > 0.5:
            cursor.execute(self.job_query, ("20110101", "20111231"))
        if random() > 0.5:
            cursor.execute(self.job_query, ("20120101", "20121231"))
        if random() > 0.5:
            cursor.execute(self.job_query, ("20130101", "20131231"))
        if random() > 0.5:
            cursor.execute(self.job_query, ("20140101", "20141231"))
        if random() > 0.5:
            cursor.execute(self.job_query, ("20150101", "20151231"))