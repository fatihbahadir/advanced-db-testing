
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import cursor
from threading import get_ident
from random import random

from modules.worker.base_worker import WorkerManager

class BWorkerManager(WorkerManager):

    def __init__(self, 
                 worker_amount: int, 
                 connection_params: dict,
                 increment_complete: callable,
                 increment_deadlock: callable) -> None:
        super().__init__(worker_amount, connection_params, increment_complete, increment_deadlock)

        self.job_query = sql.SQL(""" """)

    def job(self):

        for _ in range(100):

            conn, cursor = self.connect()

            try:
                self._random_execute(cursor)
            except psycopg2.Error as e:
                self._logger.debug("DB error [worker#b]: " + e)
                if e.args[0] == 40001 or "deadlock" in e.args[1].lower():
                    self._logger.warn(f"DB deadlock [worker#b] (thread::{get_ident()})")
                    self.increment_deadlock()

            self.disconnect(conn_data=(conn, cursor))

        self.increment_complete()

    def _random_execute(self, cursor: cursor):

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