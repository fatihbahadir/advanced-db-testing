import customtkinter
from modules.screen.components.input_field import InputField
from modules.screen.components.checkbox_field import CheckBoxField
from modules.screen.components.selectbox import SelectBox
from modules.screen.pages.main_page import MainPage

from modules.screen.base import BasePage

from modules.worker.enums import TransactionIsolationLevel

class FormPage(customtkinter.CTkFrame, BasePage):
    def __init__(self, master, switch_frame_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.padx = 15
        self.pady = 10
        self.has_index = customtkinter.StringVar(value="True")
        self.transcation_level = customtkinter.StringVar(value="read uncommitted")
        self.switch_frame_callback = switch_frame_callback


        self.select_box = SelectBox(self, "Select Isolation Level", TransactionIsolationLevel.list(), "read uncommitted")
        self.select_box.pack(padx=self.padx, pady=5, fill='x')

        self.input_a = InputField(self, "Type A User Count", "Number")
        self.input_a.pack(padx=self.padx, pady=10, fill='x')

        self.input_b = InputField(self, "Type B User Count", "Number")
        self.input_b.pack(padx=self.padx, pady=10, fill='x')

        self.checkbox = CheckBoxField(
            self, 
            label_text="Create Index", 
            variable=self.has_index, 
            onvalue="True", 
            offvalue="False"
        )
        self.checkbox.pack(padx=self.padx, pady=10, fill='x')

        self.start_button = customtkinter.CTkButton(self, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(padx=self.padx, pady=20, fill='x', side='bottom')


    def start_simulation(self):        
        self.find_screen().app.start_simulation(
            int(self.input_a.get_value()),
            int(self.input_b.get_value()),
            TransactionIsolationLevel.from_value(self.select_box.get_selected_option()),
            self.checkbox.get_value() == "True"
        )
        self.switch_frame_callback()
