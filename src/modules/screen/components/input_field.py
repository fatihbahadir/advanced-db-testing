import customtkinter

class InputField(customtkinter.CTkFrame):
    def __init__(self, master, label_text, placeholder_text, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color = "transparent")
        
        self.label = customtkinter.CTkLabel(self, text=label_text)
        self.label.pack(anchor='w')

        self.input = customtkinter.CTkEntry(self, placeholder_text=placeholder_text)
        self.input.pack(pady=10, fill='x')

    def get_value(self):
            return self.input.get()