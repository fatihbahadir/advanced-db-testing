import customtkinter

class InfoLabel(customtkinter.CTkFrame):
    def __init__(self, master, label_text, value_text, row, **kwargs):
        super().__init__(master, **kwargs)


        label = customtkinter.CTkLabel(self, text=label_text, width= 200, anchor='w')
        label.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=(10, 0))

        self.value_label = customtkinter.CTkLabel(self, text=value_text, font=("Arial", 22, "bold"), anchor='w')
        self.value_label.grid(row=1, column=0, sticky="ew", padx=(10, 5), pady=(0, 10))

    def set_value(self, value: int) -> None:
        self.value_label.configure(text = value)


