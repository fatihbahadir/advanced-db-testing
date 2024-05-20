import customtkinter

class CheckBoxField(customtkinter.CTkFrame):
    def __init__(self, master, label_text, variable, onvalue, offvalue, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color = "transparent")

        self.variable = variable
        self.checkbox = customtkinter.CTkCheckBox(self, text=label_text, variable=variable, onvalue=onvalue, offvalue=offvalue)
        self.checkbox.pack(fill='x')

    def get_value(self):
        # Checkbox'un seçili durumunu döndür
        return self.variable.get()