
from datetime import datetime
import time
from random import random
from threading import Event, get_ident

from modules.screen.screen import Screen
from modules.screen.enums import ScreenStatus
from core.app_enums import ApplicationStatus
from core.app_logger import Logger
from core.utils.thread_utils import StoppableThread

from modules.worker.enums import TransactionIsolationLevel
from modules.worker.worker_a import AWorkerManager
from modules.worker.worker_b import BWorkerManager
from services.db_connector import DbConnector

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.screen.screen import Screen

class App:

    _instance: "App" = None
    _screen: "Screen" = None

    _is_app_running = False
    _app_status = None

    _app_cycle_thread = None
    _simulation_thread = None

    _logger = Logger(__name__).get_logger()

    form_data = {}

    a_worker_manager: AWorkerManager = None
    b_worker_manager: BWorkerManager = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def start(self):
        self._initialize()
        self._screen.mainloop()

    def stop(self):
        self._is_app_running = False
        self._app_status = ApplicationStatus.CLOSING

        self._app_cycle_thread.stop()
        self._app_cycle_thread.join()

        if self._simulation_thread:
            self._simulation_thread.join()

        self._screen.destroy()

    def info(self):
        self._logger.info("\n$ App Info ~ " + str(datetime.now()))
        self._logger.info("App State: " + self._app_status.name)
        self._screen.info()
        self._logger.info("$ ------------------------ > #\n")

    def start_simulation(self, a_amount: int, b_amount: int, level: TransactionIsolationLevel, is_indexed: bool):
        if self._app_status != ApplicationStatus.IDLE:
            self._logger.warn("App status must be IDLE to start simulation. current: " + self._app_status.name)
            return

        if self._screen._screen_status != ScreenStatus.BLOCKED:
            self._logger.warn("Screen status must be IDLE to start simulation. current: " + self._screen._screen_status.name)

        self._set_simulation_form_data(a_amount, b_amount, level, is_indexed)
        self._screen.callbacks["set_initial_params"](self.form_data)
        
        self._screen.switch_dashboard()

        self._start_simulation()

    def refresh(self):

        self.form_data = {}

        self._simulation_thread = None

        self.a_worker_manager = None
        self.b_worker_manager = None

    def panic(self):
        self._logger.warn("System panicked!!")
        self._app_status = ApplicationStatus.CRASHED

    def _initialize(self):
        self._is_app_running = True
        self._app_status = ApplicationStatus.IDLE

        self._screen = Screen(app=self,
                              geometry="400x400",
                              title="Form")
        self._app_cycle_thread = StoppableThread(target=self._run_cycle_thread)
        self._app_cycle_thread.start()

    def _run_cycle_thread(self, stop_event: Event):

        while self._is_app_running:

            self.info()
            self._health_check()

            for _ in range(30):
                if stop_event.is_set(): break
                time.sleep(1)

    def _health_check(self):

        if self._app_status == ApplicationStatus.CRASHED:
            self._logger.warn("Application Status :: CRASHED")
            self.panic()
            return

        if self._screen._screen_status == ScreenStatus.CRASHED:
            self._logger.warn("Screen Status :: CRASHED")
            self.panic()
            return

    def _set_status(self, status: ApplicationStatus) -> None:
        if isinstance(status, ApplicationStatus):
            self._app_status = status

    def _set_simulation_form_data(self, a_amount: int, b_amount: int, level: TransactionIsolationLevel, is_indexed: bool) -> None:
        self.form_data = {
            "a_amount": a_amount,
            "b_amount": b_amount,
            "level": level,
            "is_indexed": is_indexed}

    def _start_simulation(self):
        
        if self._simulation_thread is not None:
            self._logger.warn("Application can not execute two simulation simultaneously")
            return
        
        self._simulation_thread = StoppableThread(target=self._simulate)
        self._simulation_thread.start()

    def _stop_simulation(self):

        self._simulation_thread.stop()
        self.a_worker_manager.stop()
        self.b_worker_manager.stop()

        self._app_status = ApplicationStatus.IDLE
        self._screen._screen_status = ScreenStatus.IDLE
        self._screen.callbacks["remove_progress_bar"]()

        self._simulation_thread = None
        
        self.a_worker_manager = None
        self.a_worker_manager = None

    def _simulate(self, stop_event: Event):
        
        self._app_status = ApplicationStatus.RUNNING

        ##### worker setup
        self._init_workers()
        self.a_worker_manager.start()
        self.b_worker_manager.start()
        #####

        self._stop_simulation()

    def _init_workers(self):

        self.a_worker_manager = AWorkerManager(
            worker_amount=self.form_data["a_amount"],
            increment_complete=self._screen.callbacks["increment_a_completed"],
            increment_deadlock=self._screen.callbacks["increment_a_deadlock"],
            set_average=self._screen.callbacks["set_a_average"])
        
        self.b_worker_manager = BWorkerManager(
            worker_amount=self.form_data["b_amount"],
            increment_complete=self._screen.callbacks["increment_b_completed"],
            increment_deadlock=self._screen.callbacks["increment_b_deadlock"],
            set_average=self._screen.callbacks["set_b_average"])
