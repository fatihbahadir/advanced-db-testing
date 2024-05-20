 
import customtkinter
from .pages.form_page import FormPage
from .pages.main_page import MainPage

from modules.screen.enums import ScreenStatus
from core.app_logger import Logger

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.application import App

class Screen(customtkinter.CTk):

    _logger = Logger(__name__).get_logger()

    def __init__(self, app: "App", geometry: str, title: str ) -> None:
        
        super().__init__()
        self.geometry(geometry)
        self.title(title)
        self.resizable(False, False)

        self.app = app
        self._screen_status = ScreenStatus.BLOCKED

        self.callbacks = {
            "increment_a_completed": None,
            "increment_b_completed": None,
            "increment_a_deadlock" : None,
            "increment_b_deadlock" : None,
            "set_a_average" : None,
            "set_b_average" : None,
            "set_initial_params": None,
            "remove_progress_bar": None,
        }

        self.main_page = MainPage(master=self)
        # Main Page
        self.form_page = FormPage(master=self, switch_frame_callback = self.switch_dashboard)
        self.form_page.pack(fill='both', expand=True)

        # Bind Protocol
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def info(self):
        print("Screen Geometry HxW]: "+ self.geometry())
        print("Screen Status (ScreenStatus#ENUM): " +self._screen_status.name)
  
    def start(self):
        pass

    def switch_dashboard(self) -> None:
        self.form_page.pack_forget()
        self.main_page.pack(fill='both', expand=True)
        self.resize_screen()
    
    def switch_form(self) -> None:
        self.main_page.pack_forget()
        self.form_page.pack(fill='both', expand=True)
        self.resize_screen()

    def _set_status(self, status: ScreenStatus) -> None:
        if isinstance(status, ScreenStatus):
            self._screen_status = status

    def resize_screen(self):
        self.geometry("500x450")

    def set_callbacks(self, callbacks: dict):
        self.callbacks = callbacks
  
    def _on_close(self):
        self.app.stop()