import customtkinter

class SelectBox(customtkinter.CTkFrame):
    def __init__(self, master, label_text, options, default_value, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(fg_color = "transparent")
        
        self.label = customtkinter.CTkLabel(self, text=label_text)
        self.label.pack(pady=(10, 0), anchor='w')

        self.selected_option = customtkinter.StringVar(value=default_value)
        self.selectbox = customtkinter.CTkOptionMenu(self,
                                                     variable=self.selected_option,
                                                     fg_color="#353739",
                                                     button_color="#4C5153",
                                                     values=options)
        self.selectbox.pack(pady=(0, 10), fill='x')

    def get_selected_option(self):
        # Seçili seçeneği döndür
        return self.selected_option.get()