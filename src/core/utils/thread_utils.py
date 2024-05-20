
import threading
import time

class StoppableThread(threading.Thread):
    def __init__(self, target, *args, **kwargs):
        super().__init__()
        self._stop_event = threading.Event()
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._kwargs['stop_event'] = self._stop_event

    def run(self):
        while not self._stop_event.is_set():
            self._target(*self._args, **self._kwargs)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()