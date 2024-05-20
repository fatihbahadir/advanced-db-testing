import customtkinter

class CustomProgressBar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Progress bar bileşeni oluştur
        self.progress_bar = customtkinter.CTkProgressBar(self)
        self.progress_bar.pack(fill="x", padx=10, pady=10)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()


