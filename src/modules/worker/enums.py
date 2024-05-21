
from enum import Enum

class TransactionIsolationLevel(Enum):
    
    READ_UNCOMMITTED = "read uncommitted"
    READ_COMMITTED = "read committed"
    REPEATABLE_READ = "repeatable read"
    SERIALIZABLE = "serializable"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
    @classmethod
    def from_value(cls, value):
        for level in cls:
            if level.value == value:
                return level
        raise ValueError("Invalid transaction isolation level: {}".format(value))