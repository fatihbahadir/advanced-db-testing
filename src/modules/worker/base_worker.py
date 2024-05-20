
import psycopg2
from psycopg2.extensions import connection, cursor
from threading import Thread, get_ident

from abc import ABC, abstractmethod

from typing import List, Tuple

from core.app_logger import Logger

class IWorkerManager(ABC):

    @abstractmethod
    def connect(self) -> Tuple[connection, cursor]:
        """Connect to database"""

    @abstractmethod
    def disconnect(self, conn_data: Tuple[connection, cursor]) -> None:
        """Disconnect from database"""

    @abstractmethod
    def initialize(self):
        """Initialize threads instance"""

    @abstractmethod
    def start(self):
        """Start executing threads job()'s"""

    @abstractmethod
    def job(self):
        """A job of one individual thread requested to do"""

class WorkerManager(IWorkerManager):

    _logger = Logger(__name__).get_logger()

    def __init__(self, 
                 worker_amount: int,
                 connection_params: dict,
                 increment_complete: callable,
                 increment_deadlock: callable) -> None:
        self.worker_amount = worker_amount
        self.connection_params = connection_params
        self.increment_complete = increment_complete
        self.increment_deadlock = increment_deadlock

        self._threads: List[Thread] = []

        self.number_of_deadlocks = 0

        self.job_query = None

    def __del__(self):
        self._clear_threads()
        self._logger.debug(f"{self.__class__.__name__} destroyed")

    def connect(self) -> Tuple[connection, cursor]:
        try:
            conn = psycopg2.connect(**self.connection_params)
            cursor = self.db_conn.cursor()
        except psycopg2.Error as e:
            self._logger.error("DB connection error: " + e)
            raise
        self._logger.debug(f"DB connection successful (thread::{get_ident()})")
        return (conn, cursor)

    def disconnect(self, conn_data: Tuple[connection, cursor]) -> None:
        conn, cursor = conn_data
        if cursor:
            cursor.close()
            cursor = None
            self._logger.debug(f"DB cursor closed (thread::{get_ident()})")
        if conn:
            conn.close()
            conn = None
            self._logger.debug(f"DB conn closed (thread::{get_ident()})")

    def initialize(self):
        self._clear_threads()
        for _ in self.worker_amount:
            self._threads.append(Thread(target=self.job))

    def start(self):
        if self._threads:
            for t in self._threads:
                t.start()

    def job(self):
        raise NotImplementedError(f"{self.__class__.__name__}.job() not implemented")

    def _clear_threads(self):
        
        for t in self._threads:
            self._logger.debug(f"Thread ({t.getName()}) joining..")
            t.join()
            self._logger.debug(f"Thread ({t.getName()}) joined")
        self._threads = []
        self._logger.debug("self._threads cleared")
