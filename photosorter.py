# used to do the actual sorting
from sorter import Sorter

# used for gui
import customtkinter as cs

from time import time


class Photosorter(cs.CTk):
    def __init__(self):
        super().__init__()

        # Windows options
        self.title("PhotoSorter")
        self.iconbitmap("./images.ico")
        self.minsize(600, 450)
        self.resizable(True, True)

        # customTkinter variables
        # Labels
        self.title_label: cs.CTkLabel = cs.CTkLabel(self)
        self.explaination_label: cs.CTkLabel = cs.CTkLabel(self)

        # Entries
        self.old_img_dir_entry: cs.CTkEntry = cs.CTkEntry(self)

        # draw(?) the main window
        self.main_window()

    def main_window(self):
        """Initiates the main labels, buttons and buttons of the window"""
        # configure the grid
        for i in range(10):
            self.rowconfigure(i, weight=1)

        # title
        self.title_label = cs.CTkLabel(
            self,
            text="Bienvenue dans le trieur de photo",
            font=("Arial", 20, 'bold'),
            height=2,
            # sticky="news"
        )
        self.title_label.grid(row=0, column=0)

        # explaination of the entry below it (old_img_dir)
        self.explaination_label = cs.CTkLabel(
            self,
            text="Mettre ici le chemin de vos photos",
            font=("Arial", 15, 'bold'),
            height=2
        )
        self.explaination_label.grid(row=1, column=0)


if __name__ == '__main__':
    app = Photosorter()
    app.mainloop()
