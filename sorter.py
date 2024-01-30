import os  # used to remove files

import pathlib  # used to manage paths
import shutil  # used to move files
from datetime import datetime

import PIL.Image  # used to get metadata


class Sorter:
    def __init__(self):
        # Initialisation of the variables
        self.accepted_img_extensions: tuple = (".png", ".jpg", ".jpeg", ".raw", ".gif", ".jpe", ".jif", ".jfif")

        # path for the image being sorted
        self.new_img_path: pathlib.Path = pathlib.Path()  # Where the image will be after being sorted
        self.current_img_path: pathlib.Path = pathlib.Path()  # Where the image is before being sorted
        # calculated date for image being sorted
        self.date_of_image: datetime = datetime(1970, 1, 1)

        # program related paths
        self.program_path: pathlib.Path = os.path.abspath(__file__)  # Absolute path of the program
        self.program_name: str = ""  # name of the program
        self.get_program_name()

        # Directory that contains the images to sort. Default = where the program is
        self.original_img_directory: pathlib.Path = self.get_directory("Where are the images to sort ? ")
        # Directory that will contain the sorted images. Default = where the program is
        self.new_img_directory: pathlib.Path = self.get_directory(
            "Where do you want the program to put the sorted images ?", False)
        if self.new_img_path == pathlib.Path(""):
            self.new_img_directory = self.original_img_directory
        # way of sorting photos
        # TODO: change its name to more clear one
        self.sorting_manner: str = input("How would you like to sort the photos ? ")
        # if none is given, this is the default way
        if self.sorting_manner == '':
            self.sorting_manner = "year + s + year + '_' + month + '_' + day"

        self.run()

    def get_program_name(self):
        """
        The get_program_name function takes the program_path and removes any trailing slash, then returns the basename of
        the path to set self.program_name to the name of the program ex: "sorter.py"

        :return: Nothing
        """
        self.program_name = self.program_path
        self.program_name = os.path.normpath(self.program_name)  # removes any trailing slash
        self.program_name = os.path.basename(self.program_name)  # get everything after the last slash

    def run(self):
        img_counter: int = 0
        for file in self.original_img_directory.iterdir():
            # check if it's an image
            for extension in self.accepted_img_extensions:
                if str(file).lower().endswith(extension):  # .lower() is used since some files are .JPG instead of .jpg
                    img_counter += 1
                    self.current_img_path = file
                    self.get_img_metadata()
                    self.get_new_img_path()
                    break

        # if there wasn't any image
        if not img_counter:
            print("\nERROR, the first given path does not contain any image.")

    @staticmethod
    def mkdir(path_to_create: pathlib.Path):
        """
        The mkdir function creates a directory.
        Any non-existent parent folders will be created

        :param: path_to_create The path that will be created
        :return: Nothing
        """
        path_to_create.mkdir(parents=True, exist_ok=True)

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
        self.mkdir(self.new_img_path)
        try:
            shutil.move(self.current_img_path, self.new_img_path)
        except shutil.Error:  # delete the file if it already exists where you want to move it
            self.delete_image()

    def get_directory(self,
                      input_str: str,
                      need_to_exist: bool = True):
        """
        The get_directory function asks the user for a directory path to where the images are located.
        If the user didn't specify any path, the path of the program is used
        directory_var must already have a default path

        :param: input_str the string to put in the input method
        :param: need_to_exist Does the path needs to exist or will it be created
        :return: the path
        """
        result_to_return: pathlib.Path = pathlib.Path("./")
        tmp_input: str = input(input_str)

        if tmp_input:
            result_to_return = pathlib.Path(tmp_input)

        # test the path
        if need_to_exist and not result_to_return.exists():
            print(f"\nERROR, the specified path does not exists.\nSpecified path : \"{tmp_input}\"")
            exit(0)
        elif not need_to_exist and not result_to_return.exists():
            self.mkdir(result_to_return)

        return result_to_return

    def get_img_metadata(self):
        current_image: PIL.Image = PIL.Image.open(self.current_img_path)
        current_image_metadata: PIL.Image.Exif = current_image.getexif()

        date: str
        date_list: list[str]

        # trying different values known to contain the date of the photo
        try:
            date = current_image_metadata[36868]
        except KeyError:
            try:
                date = current_image_metadata[306]
            except KeyError:
                date = None
        except TypeError:
            date = None

        if date is not None:
            date_list = date.split(":")
            self.date_of_image = datetime(
                year=int(date_list[0]),
                month=int(date_list[1]),
                day=int(date_list[2][:2]),
            )
        else:
            self.date_of_image = None

    def get_new_img_path(self):
        #
        if self.date_of_image is None:
            self.new_img_path = self.new_img_directory.joinpath(pathlib.Path("/Inclassable"))
            print(self.new_img_path.absolute())
            return

        sorting_array: list = self.sorting_manner.split("+")
        tmp_str: str = ""  # used to store the temporary directory name

        # TODO: transformer self.date_of_image en dico

        for string in sorting_array:
            if string.strip == "s":
                self.new_img_path = self.new_img_path.joinpath(tmp_str)
                tmp_str = ""
                continue
            if string.strip in self.date_of_image:
                tmp_str += self.date_of_image[string.strip]
            else:
                tmp_str += string

        print(self.new_img_path.absolute())


