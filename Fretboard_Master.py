import customtkinter as ctk
from Screen import Screen

if __name__ == "__main__":
    app = ctk.CTk()
    screen = Screen(app)
    screen.main_screen()
    app.mainloop()
