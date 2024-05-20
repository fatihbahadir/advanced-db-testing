
from abc import ABC, abstractmethod

from typing import List

from core.app_logger import Logger
from core.utils.thread_utils import StoppableThread

class IWorkerManager(ABC):

    @abstractmethod
    def initialize(self):
        """Initialize threads instance"""

    @abstractmethod
    def start(self):
        """Start executing threads job()'s"""

    @abstractmethod
    def stop(self):
        """Stop executing remain jobs"""

    @abstractmethod
    def job(self):
        """A job of one individual thread requested to do"""

class WorkerManager(IWorkerManager):

    _logger = Logger(__name__).get_logger()

    def __init__(self, 
                 worker_amount: int,
                 increment_complete: callable,
                 increment_deadlock: callable,
                 set_average: callable) -> None:
        self.worker_amount = worker_amount
        self.increment_complete = increment_complete
        self.increment_deadlock = increment_deadlock
        self.set_average = set_average

        self._threads: List[StoppableThread] = []

        self.total_elapsed_time_per_worker: float = 0.0
        self.number_of_deadlocks = 0

        self.job_query = None

    def __del__(self):
        self._clear_threads()
        self._logger.debug(f"{self.__class__.__name__} destroyed")

    def initialize(self):
        self._clear_threads()
        for _ in self.worker_amount:
            self._threads.append(StoppableThread(target=self.job))

    def start(self):
        self.initialize()

        if self._threads:
            for t in self._threads:
                t.start()

        for t in self._threads:
            t.join()

    def stop(self):
        for t in self._threads:
            t.stop()
        for t in self._threads:
            t.join()

    def job(self):
        raise NotImplementedError(f"{self.__class__.__name__}.job() not implemented")

    def _clear_threads(self):
        
        for t in self._threads:
            self._logger.debug(f"Thread ({t.getName()}) joining..")
            t.join()
            self._logger.debug(f"Thread ({t.getName()}) joined")
        self._threads = []
        self._logger.debug("self._threads cleared")

    def _update_ui(self):

        self.set_average(round(self.total_elapsed_time_per_worker / self.worker_amount , 2))
        self.increment_complete()

    def _deadlock_occured(self):

        self.number_of_deadlocks +=  1
        self.increment_deadlock()