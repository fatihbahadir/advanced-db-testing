import customtkinter
from modules.screen.components.info_label import InfoLabel
from modules.screen.components.progress_bar import CustomProgressBar

from modules.screen.base import BasePage

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.screen.screen import Screen

class MainPage(customtkinter.CTkFrame, BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.a_complete_amount = 0
        self.b_complete_amount = 0
        self.a_deadlock_amount = 0
        self.b_deadlock_amount = 0
        self.a_average_count = 0
        self.b_average_count = 0


        self.screen = self.find_screen()
        
        self.form_data = {}
        
        self.screen.set_callbacks(callbacks = {
            "increment_a_completed": self.increment_a_completed,
            "increment_b_completed": self.increment_b_completed,
            "increment_a_deadlock": self.increment_a_deadlock,
            "increment_b_deadlock": self.increment_b_deadlock,
            "set_a_average": self.set_a_average,
            "set_b_average": self.set_b_average,
            "set_initial_params": self.set_initial_params,
            "remove_progress_bar": self.remove_progress_bar
        })

        self.data = self.screen.app.form_data
 
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.grid_columnconfigure(0, weight=1)  
        self.grid_columnconfigure(1, weight=1)

        type_a_label = customtkinter.CTkLabel(self, text="Type A", font=("Arial", 30, "bold"))
        type_a_label.grid(row=0, column=0, sticky="w", padx=20, pady=5)

        self.completed_threads_info_a = InfoLabel(self, "Number of completed threads", f"0 / 0", 1)
        self.completed_threads_info_a.grid(row=1, column=0)

        self.deadlocks_info_a = InfoLabel(self, "Number of deadlocks", "0", 3)
        self.deadlocks_info_a.grid(row=3, column=0)

        self.average_duration_info_a = InfoLabel(self, "Average Duration", "10ms", 5)
        self.average_duration_info_a.grid(row=5, column=0)

        self.type_b_label = customtkinter.CTkLabel(self, text="Type B", font=("Arial", 30, "bold"))
        self.type_b_label.grid(row=0, column=1, sticky="w", padx=20, pady=5)

        self.completed_threads_info_b = InfoLabel(self, "Number of completed threads", "0 / 0", 1)
        self.completed_threads_info_b.grid(row=1, column=1)

        self.deadlocks_info_b = InfoLabel(self, "Number of deadlocks", "0", 3)
        self.deadlocks_info_b.grid(row=3, column=1)

        self.average_duration_info_b = InfoLabel(self, "Average Duration", "10ms", 5)
        self.average_duration_info_b.grid(row=5, column=1)

        self.progress_bar = CustomProgressBar(self)
        self.progress_bar.grid(row=7, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

    
    def increment_a_completed(self):
        self.a_complete_amount += 1
        self.completed_threads_info_a.set_value(f"{self.a_complete_amount} / {self.form_data['a_amount']}")

    def increment_b_completed(self):
        self.b_complete_amount += 1
        self.completed_threads_info_b.set_value(f"{self.b_complete_amount} / {self.form_data['b_amount']}")

    def increment_a_deadlock(self):
        self.a_deadlock_amount += 1
        self.deadlocks_info_a.set_value(self.a_deadlock_amount)

    def increment_b_deadlock(self):
        self.b_deadlock_amount += 1
        self.deadlocks_info_b.set_value(self.b_deadlock_amount)

    def set_a_average(self):
        pass

    def set_b_average(self):
        pass

    def set_initial_params(self, data: dict):
        self.form_data = data
        self.completed_threads_info_a.set_value(f"0 / {self.form_data['a_amount']}")
        self.completed_threads_info_b.set_value(f"0 / {self.form_data['b_amount']}")
    
    def remove_progress_bar(self):
        self.progress_bar.grid_remove()
        self.add_buttons()
    
    def add_buttons(self):
        self.save_button = customtkinter.CTkButton(self, text="Save Results", command=self.save_results)
        self.save_button.grid(row=7, column=0, pady=20, padx=20, sticky="ew")

        self.restart_button = customtkinter.CTkButton(self, text="Restart", command=self.restart)
        self.restart_button.grid(row=7, column=1, pady=20, padx=20, sticky="ew")    
    
    def save_results(self):
        print("Results saved!")

    def restart(self):
        self.screen.switch_form()