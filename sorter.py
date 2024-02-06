import os  # used to remove files

import pathlib  # used to manage paths
import shutil  # used to move files
from datetime import datetime  # used to store date data

import PIL.Image  # used to get metadata


class Sorter:
    def __init__(self, app):
        self.app = app
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
        # self.original_img_directory: pathlib.Path = self.get_directory("Where are the images to sort ? ")
        self.original_img_directory: pathlib.Path = pathlib.Path("./")
        # Directory that will contain the sorted images. Default = where the program is
        # self.new_img_directory: pathlib.Path = self.get_directory(
        #     "Where do you want the program to put the sorted images ?", False)
        self.new_img_directory: pathlib.Path = pathlib.Path("./")
        if self.new_img_path == pathlib.Path(""):
            self.new_img_directory = self.original_img_directory
        # way of sorting photos
        # TODO: change its name to more clear one
        # self.sorting_manner: str = input("How would you like to sort the photos ? ")
        self.sorting_manner: str = ''
        # if none is given, this is the default way
        if self.sorting_manner == '':
            self.sorting_manner = "year+s+year+_+month+_+day"

        self.img_counter: int = 0  # counts the number of sorted images
        self.img_number: int = 0  # number of images to sort

        # self.run()

    def get_program_name(self) -> None:
        """
        The get_program_name method takes the program_path and removes any trailing slash, then returns the basename of
        the path to set self.program_name to the name of the program ex: "sorter.py"
        """
        self.program_name = self.program_path
        self.program_name = os.path.normpath(self.program_name)  # removes any trailing slash
        self.program_name = os.path.basename(self.program_name)  # get everything after the last slash

    def run(self) -> None:
        """
        The run method gathers the other methods to sort all the images in the directory
        """
        self.img_number = self.get_img_number()
        for file in self.original_img_directory.iterdir():
            # check if it's an image
            for extension in self.accepted_img_extensions:
                if str(file).lower().endswith(extension):  # .lower() is used since some files are .JPG instead of .jpg
                    self.img_counter += 1  # update the number of images processed
                    self.current_img_path = file
                    self.get_img_metadata()  # get the date of the image
                    self.get_new_img_path()
                    self.moving()
                    self.calculate_progress()

        # if there wasn't any image
        if not self.img_counter:
            if not self.app.warning_is_displayed:
                self.app.warning()

    @staticmethod
    def mkdir(path_to_create: pathlib.Path) -> None:
        """
        The mkdir method creates a directory.
        Any non-existent parent folders will be created

        :param path_to_create: The path that will be created
        """
        path_to_create.mkdir(parents=True, exist_ok=True)

    def delete_image(self) -> None:
        """
        The delete method removes the specified image from the directory.
        """
        os.remove(self.current_img_path)

    def moving(self) -> None:
        """
        The moving method moves a file to a new location.
        It takes two arguments: the file to move and the path where it will be moved.
        This method creates any necessary directories in order for the file to be moved there using another method.
        """
        self.mkdir(self.new_img_path)
        try:
            shutil.move(self.current_img_path, self.new_img_path)
        except shutil.Error:  # delete the file if it already exists where you want to move it
            self.delete_image()

    def get_img_metadata(self) -> None:
        """
        Retrieve the metadata of the image and save it into self.date_of_image to be used later
        """
        current_image: PIL.Image = PIL.Image.open(self.current_img_path)
        current_image_metadata: PIL.Image.Exif = current_image.getexif()

        date: str | None
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

        # if a date was found
        if date is not None:
            date_list = date.split(":")
            self.date_of_image = datetime(
                year=int(date_list[0]),
                month=int(date_list[1]),
                day=int(date_list[2][:2]),
                hour=int(date_list[2][3:]),
                minute=int(date_list[3]),
                second=int(date_list[4])
            )
        else:
            self.date_of_image = None

    def get_new_img_path(self) -> None:
        """
        Calculate the new image path using the sorting way chose by the user
        and put it in self.new_img_path
        """
        # if the date wasn't found
        if self.date_of_image is None:
            # TODO: add a option to let the user choose the name of that directory
            self.new_img_path = self.new_img_directory.joinpath(pathlib.Path("/Unclassifiable"))
            return

        sorting_array: list[str] = self.sorting_manner.split("+")  # list of the different component of the sorting way
        tmp_str: str = ""  # used to store the temporary directory name

        # used for simplicity of code (iterating through each key, which is not possible with datetime object
        # TODO: maybe add hours and minutes or more ?
        date: dict = {
            "year": self.date_of_image.year,
            "month": self.date_of_image.month,
            "day": self.date_of_image.day
        }
        self.new_img_path = self.new_img_directory  # set the beginning of the new image path

        # iterate through each component of the sorting way
        for string in sorting_array:
            # if user wants a new folder
            if string.strip() == "s":
                self.new_img_path = self.new_img_path.joinpath(tmp_str)
                tmp_str = ""
                continue
            # is user wants to put a key date
            if string.strip() in list(date.keys()):
                tmp_str += str(date[string.strip()])
            # else, any other characters are put directly in the path
            else:
                tmp_str += string
        self.new_img_path = self.new_img_path.joinpath(tmp_str)

    def set_sorting_path(self, path: pathlib.Path) -> None:
        """
        Set the path of the original directory to the parameter path

        :param path: New path of the original directory
        """
        self.original_img_directory = path
        self.new_img_directory = path

    def get_img_number(self) -> int:
        """
        :return: number of images int the original directory
        """
        num: int = 0  # number of images detected

        for file in self.original_img_directory.iterdir():
            # check if it's an image
            for extension in self.accepted_img_extensions:
                if str(file).lower().endswith(extension):  # .lower() is used since some files are .JPG instead of .jpg
                    num += 1
                    break
        return num

    def calculate_progress(self):
        """
        Calculate the progress of the sorting and updates the progress bar on the ui
        """
        progress: float = self.img_counter / self.img_number
        self.app.set_progress_bar(progress)
