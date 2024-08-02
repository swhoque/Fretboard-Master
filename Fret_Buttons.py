from customtkinter import CTkButton

class FretButton(CTkButton):
    def __init__(self, master, text, row, col, func):
        super().__init__(master,
                        text=text,
                        command=func
                        )
        self.row = row
        self.col = col
        self.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
