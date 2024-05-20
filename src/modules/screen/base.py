
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.screen.screen import Screen

class IBasePage(ABC):

    @abstractmethod
    def find_screen(self):
        """Find the most top element on hierarchy"""


class BasePage:
    
    def find_screen(self) -> "Screen":
        upper = self.master
        while (upper.master):
            upper = upper.master
        return upper