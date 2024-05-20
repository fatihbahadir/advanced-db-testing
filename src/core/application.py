from threading import Thread
from datetime import datetime
import time
from random import random

from modules.screen.screen import Screen
from modules.screen.enums import ScreenStatus
from core.app_enums import ApplicationStatus
from core.app_logger import Logger

from modules.worker.enums import TransactionIsolationLevel
from services.db_connector import DbConnector

class App:

    _instance = None
    _screen = None
    _database = None

    _is_app_running = False
    _app_status = None

    _app_cycle_thread = None
    _simulation_thread = None

    _logger = Logger(__name__).get_logger()

    curr_simulation_meta = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def start(self):
        self._initialize()
        self._screen.mainloop()

    def stop(self):
        self._is_app_running = False
        self._app_cycle_thread.join()

        self._simulation_thread.join()

        self._screen.stop()

    def info(self):
        self._logger.info("\n$ App Info ~ " + str(datetime.now()))
        self._logger.info("App State: " + self._app_status.name)
        self._screen.info()
        self._logger.info("$ ------------------------ > #\n")

    def start_simulation(self, a_amount: int, b_amount: int, level: TransactionIsolationLevel, is_indexed: bool):
        if self._app_status != ApplicationStatus.IDLE:
            self._logger.warn("App status must be IDLE to start simulation. current: " + self._app_status.name)
            return

        if self._screen._screen_status != ScreenStatus.IDLE:
            self._logger.warn("Screen status must be IDLE to start simulation. current: " + self._screen._screen_status.name)

        self._set_simulation_meta(a_amount, b_amount, level, is_indexed)
        self._screen.callbacks["set_initial_params"](self.curr_simulation_meta)
        self._screen.switch_dashboard()

        self._start_simulation()

    def refresh(self):
        pass

    def panic(self):
        self._logger.warn("System panicked!!")
        self.stop()

    def _initialize(self):
        self._is_app_running = True
        self._app_status = ApplicationStatus.IDLE

        self._screen = Screen(app=self,
                              geometry="400x400",
                              title="Form")
        self._app_cycle_thread = Thread(target=self._run_cycle_thread, daemon=True)
        self._app_cycle_thread.start()

    def _run_cycle_thread(self):

        health_counter = 0
        while self._is_app_running:
            
            if (health_counter > 5):
                self.stop()

            self.info()
            self._health_check()
            
            health_counter += 1
            print(f"Health Check: {health_counter}/5")
            time.sleep(10)

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

    def _set_simulation_meta(self, a_amount: int, b_amount: int, level: TransactionIsolationLevel, is_indexed: bool) -> None:
        self.curr_simulation_meta = {
            "a_amount": a_amount,
            "b_amount": b_amount,
            "level": level,
            "is_indexed": is_indexed}

    def _start_simulation(self):
        
        if self._simulation_thread is not None:
            self._logger.warn("Application can not execute two simulation simultaneously")
            return
        
        self._simulation_thread = Thread(target=self._simulate)
        self._simulation_thread.start()

    def _simulate(self):
        
        self._app_status = ApplicationStatus.RUNNING

        ##### worker setup
        for _ in range(10):
            self._screen.callbacks["increment_a_completed"]()
            time.sleep(random()*3)
        #####

        self._stop_simulation()

    def _stop_simulation(self):
        
        self._simulation_thread.join()
        self._simulation_thread = None

        # self._screen.simulate_result()

        self._app_status = ApplicationStatus.IDLE