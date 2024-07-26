import customtkinter as ctk
from Screen import Screen

if __name__ == "__main__":
    root = ctk.CTk()
    app = Screen(root)
    app.main_screen()
    root.mainloop()
