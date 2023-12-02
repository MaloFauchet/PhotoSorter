import os  # used to remove files
import sys  # used to know the program name

import pathlib  # used to manage paths
import shutil  # used to move files


class Sorter:
    def __init__(self):
        # Initialisation of the variables
        self.accepted_img_extensions = [".png", ".jpg", ".jpeg", ".raw", ".gif", ".jpe", ".jif", ".jfif"]

        self.new_img_path: pathlib.Path = None  # Where the image will be after being sorted
        self.current_img_path: pathlib.Path = None  # Where the image is before being sorted

        self.program_path: pathlib.Path = os.path.abspath(__file__)  # Absolute path of the program
        self.program_name: str = None  # name of the program
        self.get_program_name()

        # Directory that contains the images to sort. Default = where the program is
        self.original_img_directory: pathlib.Path = pathlib.Path(self.program_path[:len(self.program_path) - len(self.program_name)])

        self.get_program_name()
        self.get_original_img_directory()
        self.run()

    def get_program_name(self):
        """
        The get_program_name function takes the program_path and removes any trailing slash, then returns the basename of
        the path in order to set self.program_name to the name of the program ex: "sorter.py"

        :return: Nothing
        """
        self.program_name = self.program_path
        self.program_name = os.path.normpath(self.program_name)  # removes any trailing slash
        self.program_name = os.path.basename(self.program_name)  # get everything after the last slash

    def run(self):
        for file in self.original_img_directory.iterdir():
            print(file)

    def mkdir(self):
        """
        The mkdir function creates a directory.
        Any non existant subfolders will be created

        :return: Nothing
        """
        self.new_img_path.mkdir(parents=True, exist_ok=True)

    def delete_image(self):
        """
        The delete function removes the specified image from the directory.

        :return: Nothing
        """
        os.remove(self.current_img_path)

    def moving(self):
        """
        The moving function moves a file to a new location.
        It takes two arguments: the file to move and the path where it will be moved.
        The function creates any necessary directories in order for the file to be moved there using another function.

        :return: Nothing
        """
        self.mkdir()
        try:
            shutil.move(self.current_img_path, self.new_img_path)
        except shutil.Error:  # delete the file if it already exists where you want to move it
            self.delete()

    def get_original_img_directory(self):
        """
        The get_original_img_directory function asks the user for a directory path to where the images are located.
        If the user didn't specify any path, the path of the program is used

        :return: Nothing
        """
        tmp_input = input("Where are the images to sort ? ")
        if tmp_input:
            self.original_img_directory = pathlib.Path(tmp_input)

        # test path
        if not self.original_img_directory.exists():
            print(f"\nERROR, the specified path does not exists.\nSpecified path : \"{tmp_input}\"\n")
