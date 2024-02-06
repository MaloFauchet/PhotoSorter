# used to do the actual sorting

# used to get the program path
import pathlib

# used to begin the sorting
import threading
from tkinter import filedialog

# used for gui
import customtkinter as cs

from sorter import Sorter


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
        self.explanation_label: cs.CTkLabel = cs.CTkLabel(self)
        self.sort_label: cs.CTkLabel = cs.CTkLabel(self)
        self.help_sort_label: cs.CTkLabel = cs.CTkLabel(self)
        self.warning_label: cs.CTkLabel = cs.CTkLabel(self)

        # Entries
        self.old_img_dir_entry: cs.CTkEntry = cs.CTkEntry(self)
        self.sort_entry: cs.CTkEntry = cs.CTkEntry(self)

        # Buttons
        self.old_img_dir_btn: cs.CTkButton = cs.CTkButton(self)
        self.sort_help_button: cs.CTkButton = cs.CTkButton(self)
        self.launch_sort_specific_path: cs.CTkButton = cs.CTkButton(self)
        self.launch_sort_btn: cs.CTkButton = cs.CTkButton(self)

        # Progress Bar
        self.progress_bar = cs.CTkProgressBar(self)

        # Algo variables
        self.help_is_displayed: bool = False
        self.warning_is_displayed: bool = False

        # draw(?) the main window
        self.main_window()

    def main_window(self) -> None:
        """Initiates the main labels, buttons and buttons of the window"""
        # configure the grid
        for i in range(10):
            self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        # title
        self.title_label = cs.CTkLabel(
            self,
            text="Welcome in the PhotoSorter",
            font=("Arial", 20, 'bold'),
            height=2
        )
        self.title_label.grid(row=0, column=0, sticky="ew")

        # explanation of the entry below it (old_img_dir)
        self.explanation_label = cs.CTkLabel(
            self,
            text="Put here the path to you images",
            font=("Arial", 15, 'bold'),
        )
        self.explanation_label.grid(row=1, column=0)

        # manual entry of the directory containing the images
        self.old_img_dir_entry = cs.CTkEntry(
            self,
            width=400
        )
        self.old_img_dir_entry.grid(row=2, column=0)
        self.old_img_dir_entry.focus()

        # pop up explorer to choose the dir containing the images
        self.old_img_dir_btn = cs.CTkButton(
            self,
            text="Choose a directory",
            height=25,
            command=self.choose_dir
        )
        self.old_img_dir_btn.grid(row=3, column=0)

        # label which explains what the next entry is for
        self.sort_label = cs.CTkLabel(
            self,
            text="Indicate here how the program will sort you photos"
                 "\n( Default: year+s+year+_+month+_+day )",
            font=('Arial', 15)
        )
        self.sort_label.grid(row=4, column=0)

        # Place where the help label will be if the sort_help_button is clicked
        self.rowconfigure(5, weight=0)

        # Make the help label appear or disappear
        self.sort_help_button = cs.CTkButton(
            self,
            text='Help',
            command=self.help_sort_label_display
        )
        self.sort_help_button.grid(row=6, column=0)

        # Entry in which the user inputs the way he wants the program the sort his images
        self.sort_entry = cs.CTkEntry(self, width=350)
        self.sort_entry.grid(row=7, column=0)

        # sort where specified button
        self.launch_sort_specific_path = cs.CTkButton(
            self,
            text="Start sorting at specified path",
            command=lambda: self.launch_sort(True)
        )
        self.launch_sort_specific_path.grid(row=8, column=0)

        # sort where program is button
        self.launch_sort_btn = cs.CTkButton(
            self,
            text="Start sorting where the program is",
            command=lambda: self.launch_sort(False)
        )
        self.launch_sort_btn.grid(row=9, column=0)

    def choose_dir(self) -> None:
        """
        Allows the user to choose the directory of the images to sort
        through a Windows Explorer window
        """
        path: str = filedialog.askdirectory(initialdir="./")
        tmp: cs.StringVar = cs.StringVar()
        tmp.set(path)
        self.old_img_dir_entry.configure(textvariable=tmp)

    def help_sort_label_display(self) -> None:
        """Display or destroy the help label"""
        if not self.help_is_displayed:
            self.rowconfigure(5, weight=1)
            self.help_sort_label = cs.CTkLabel(
                self,
                text='"year" puts the year the photo was taken, "month" the month, "day" the day.'
                     '\n "s" allow to create a new folder with the name before'
                     '\n If you want to put other characters, just put them.',
                font=('Arial', 15, 'italic')
            )
            self.help_sort_label.grid(row=5, column=0)
            self.help_is_displayed = True
        else:
            self.help_sort_label.destroy()
            self.rowconfigure(5, weight=0)
            self.help_is_displayed = False

    def warning(self) -> None:
        """
        The warning function is a function called when the user does not enter a path to the photos.
        It displays an error message and asks him to enter a path or click on another button.
        """
        self.warning_label = cs.CTkLabel(
            self,
            text="Warning, please enter a valid path to your images.\nIf the path do exists, no images were found.",
            font=("Arial", 15),
        )
        self.warning_label.grid(row=10, column=0, pady=20)
        self.warning_is_displayed = True

    def launch_sort(self, specific_path: bool) -> None:
        """
        Launch sort

        :param specific_path: True if a path is specified, False if the user wants to use the program path
        """
        if specific_path:
            path: pathlib.Path = pathlib.Path(self.old_img_dir_entry.get())
            if not path.exists():
                self.warning()
                return
        else:
            path: pathlib.Path = pathlib.Path("./")

        sorter: Sorter = Sorter(self)
        sorter.set_sorting_path(path)

        sorting_thread: threading.Thread = threading.Thread(target=sorter.run)
        sorting_thread.start()

        if sorter.img_number != 0:
            self.progress_bar = cs.CTkProgressBar(self)
            self.progress_bar.grid(row=11, pady=20)
        else:
            self.warning()

    def set_progress_bar(self, progress: float):
        self.progress_bar.set(progress)


if __name__ == '__main__':
    app = Photosorter()
    app.mainloop()
