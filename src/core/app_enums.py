from enum import Enum

class ApplicationStatus(Enum):

    IDLE = "idle"
    RUNNING = "running"
    CRASHED = "crashed"
    