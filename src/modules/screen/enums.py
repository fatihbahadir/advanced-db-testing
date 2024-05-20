from enum import Enum

class ScreenStatus(Enum):
    
    IDLE = "idle"
    BLOCKED = "blocked"
    CRASHED = "crashed"

class CurrentPage(Enum):
    
    FORM = "form"
    DASHBOARD = "dasboard"