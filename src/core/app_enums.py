from enum import Enum

class ApplicationStatus(Enum):

    IDLE = "idle"
    RUNNING = "running"
    CLOSING = "closing"
    CRASHED = "crashed"
    