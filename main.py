import os  # used for every manipulation
import pathlib  # used to find the file path
import shutil  # used to move files
import tkinter as tk  # used to make the window
import PIL.Image  # used to extract photos exif
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


class Photosorter(tk.Tk):

    def __init__(self) -> None:
        tk.Tk.__init__(self)
        # Option de la fenêtre
        self.title('Photo Sorter with EXIF')
        self.iconbitmap('images.ico')
        self.minsize(600, 450)
        self.config(background='#605B56')
        self.resizable(width=True, height=True)
        # tkinter variables
        self.greeting = tk.Label()
        self.explanation = tk.Label()
        self.entry = tk.Entry()
        self.tri_label = tk.Label()
        self.tri_aide_button = tk.Button()
        self.tri_entry = tk.Entry()
        self.launchpath = tk.Button()
        self.launch = tk.Button()
        self.tri_label3 = tk.Label()
        self.tri_label2 = tk.Label()
        self.fnotfound = tk.Label()
        # algorithm variables
        self.testaide = False  # test if a function's already been called
        self.photolist = []  # finds all the photos and put them in this list
        self.photos_done = 0  # number of photos done
        self.imgpath = ""  # path to the image
        self.entrypath = ""  # path of the photo's folder
        self.vartri = ''  # way the program will sort photos
        self.dir_path = ""  # new path for the image
        # calling graphic method
        self.maingraph()

    def maingraph(self):
        # greeting message
        self.greeting = tk.Label(
            text="Bienvenue dans le trieur de photo",
            bg='#605B56',
            font=("Arial", 20, 'bold'),
            height='2'
        )
        self.greeting.pack()

        # path explanation
        self.explanation = tk.Label(
            text="Mettre ici le chemin de vos photos",
            bg='#605B56',
            font=("Arial", 15, 'bold'),
            height='2'
        )
        self.explanation.pack()

        # path entry
        self.entry = tk.Entry(width=75)
        self.entry.pack(padx=10, pady=10)

        # tri labels + entry
        self.tri_label = tk.Label(
            text="Indiquer ici comment le programme triera vos photos"
                 "\n( Par défault: \" year + s + year + '_' + month + '_' + day \" )",
            bg='#605B56',
            font=('Arial', 10, 'bold')
        )
        self.tri_label.pack()

        self.tri_aide_button = tk.Button(
            text='Aide',
            bg='#EBEBEB',
            command=self.aide_tri
        )
        self.tri_aide_button.pack(padx=10, pady=10)

        self.tri_entry = tk.Entry(width=65, fg="black")
        self.tri_entry.pack(padx=10, pady=10)

        # tripath button
        self.launchpath = tk.Button(
            text="Démarrer le tri au chemin spécifié",
            bg='#EBEBEB',
            command=self.get_entry_path
        )
        self.launchpath.pack()

        # tri button
        self.launch = tk.Button(text="Démarrer le tri où le programme se situe", command=self.path)
        self.launch.pack(padx=10, pady=10)

    def aide_tri(self):
        """
        The aide_tri function is used to explain how the tri function works.
        It displays a label with some text explaining how the tri function works.
        """
        if not self.testaide:
            self.tri_label2 = tk.Label(
                text='Exemple : "year + s + year + "-" + month + "-" + day" ',
                bg='#605B56',
                font=('Arial', 12)
            )
            self.tri_label2.pack()

            self.tri_label3 = tk.Label(
                text='"year" affiche l\'année de la photo, "month" le mois, "day" le jour.'
                     '\n "s" permet de créer un dossier avec le nom précédent'
                     '\n Si vous souhaitez afficher d\'autres caractères, mettez les entre guillemets.',
                bg='#605B56',
                font=('Arial', 10)
            )
            self.tri_label3.pack()
            self.testaide = True

    def warning(self):
        """
        The warning function is a function that is called when the user does not enter a path to the photos.
        It displays an error message and asks him to enter a path or click on another button.

        :return: The warning message
        """

        self.fnotfound = tk.Label(
            text="Attention, veuillez rentrez un chemin d'accès aux photos, ou cliquez sur l'autre bouton.",
            font=("Arial", 10),
            bg='#605B56',
            height='2'
        )
        self.fnotfound.pack()

    def mkdir(self):
        """
        The moving function moves a file to a new location.
        It takes two arguments: the file to move and the path where it will be moved.
        The function creates any necessary directories in order for the file to be moved there using another function.

        :return: Nothing
        """
        p = pathlib.Path(self.dir_path)
        try:
            p.mkdir(parents=True)
        except FileExistsError:  # test and print if directories already exists
            return

    def delete(self):
        """
        The delete function removes the specified image from the directory.

        :return: Nothing
        """

        os.remove(self.imgpath)
        return

    def moving(self):
        """
        The moving function moves a file to a new location.
        It takes two arguments: the file to move and the path where it will be moved.
        The function creates any necessary directories in order for the file to be moved there using another function.

        :return: Nothing
        """
        self.mkdir()
        self.dir_path = self.dir_path.replace("/", "\\")
        try:
            shutil.move(self.imgpath, self.dir_path)
        except shutil.Error:  # delete the file if it already exists where you want to move it
            self.delete()

    def path(self):
        """
        The path function finds the path of where the program is located.
        It then calls tri with this path and a user inputted variable.

        :return: The path of where the program is located
        """
        self.vartri = self.tri_entry.get()
        self.entrypath = os.path.abspath(__file__)  # find the path the python program is in
        lenprgmpath = len(self.entrypath)
        self.entrypath = self.entrypath[:lenprgmpath - 7]  # l- 21 → remove the name of the program from the path
        return

    def find(self):
        """
        The find function finds all the photos in a directory and puts them into a list.
        It also checks if there are any photos in the directory, if not it will print out an error message.

        :return: A list of all the photos in a given directory
        """
        try:
            self.photolist = [f for f in os.listdir(self.entrypath) if
                              f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG') or f.endswith(
                                  '.jpeg') or f.endswith('.mp4') or f.endswith(
                                  '.MP4')]  # find all the photos in the path
        except FileNotFoundError:
            self.warning()
            return
        return

    def get_path(self):
        """
        The get_path function takes the name of an image, its location and the value entered by the user in
        the sort entry. It then creates a path to where it should be moved based on its date. If there is no date
        in the EXIF data, it will move to a repertory called 'Inclassable';.

        :return: The path where the image will be moved
        """

        # name exemple : IMG_1068.JPG
        if self.imgpath.endswith(".mp4") or self.imgpath.endswith(".MP4"):
            videoparser = createParser(self.imgpath)
            metadata = extractMetadata(videoparser)
            date = metadata.get("creation_date")
            date = str(date)
            videoparser.close()

            year = date[0:4]  # split path into year month and day
            # month = months.get(date[5:7])  # use the dictionary 'months' to get the name of the month
            month = date[5:7]
            day = date[8:10]
            s = '/'
            self.entrypath = self.entrypath.replace("\\", "/")

            self.vartri = self.vartri.split("+")
            if self.vartri[0] == '':  # if no value was entered in the sort entry, do the default sort
                self.entrypath += s + year + s + year + '_' + month + '_' + day
                return self.entrypath

            dict_tri = {'year': year, 'month': month, 'day': day, 's': s}
            vartemp = self.entrypath + s  # go from D:/Photos2016/12-Decembre/25 to D:/Photos/2016/12-Decembre/25
            for mots in self.vartri:
                vartemp += dict_tri.get(mots)  # add value by value to form the entire path

            return vartemp

        self.imgpath = self.imgpath.replace("\\", "/")
        img = PIL.Image.open(self.imgpath)  # open the image
        exif_data = img.getexif()  # get the EXIF data of the image previously opened
        try:
            date = exif_data[36868]
        except KeyError:  # trying different values known for the date of the photo
            try:
                date = exif_data[306]
            except KeyError:
                date = None
        except TypeError:
            date = None
        img.close()  # dodge an error where the image is still used by pil and cannot be moved

        if date is None:  # if there is no date in the EXIF
            self.entrypath += "\\Inclassable"
            self.moving()  # move to the repertory inclassable
            return None

        dict_tri = {'year': date[0:4], 'month': date[5:7], 'day': date[8:10], 's': '/'}

        year = dict_tri.get('year')
        month = dict_tri.get('month')
        day = dict_tri.get('day')
        print(dict_tri)
        s = '/'
        self.entrypath = self.entrypath.replace("\\", "/")

        try:
            self.vartri = self.vartri.split("+")
        except AttributeError:
            pass
            print(self.vartri)
        if self.vartri[0] == '':  # if no value was entered in the sort entry, do the default sort
            self.entrypath += s + year + s + year + '_' + month + '_' + day
            return self.entrypath

        vartemp = self.entrypath + s  # go from D:/Photos2016/2016-12-25 to D:/Photos/2016/2016-12-25
        print(vartemp)
        for mots in self.vartri:
            print(vartemp)
            print(mots)
            print(dict_tri.get(mots))
            vartemp += dict_tri.get(mots)  # add value by value to form the entire path

        return vartemp

    def tri(self):
        """
        The tri function is the main function of the program. It calls all other functions and runs them in order to
        sort images into folders based on their date taken. The tri function also checks if there are any images in the given
        directory, if not it will show a warning message box.

        :param self: Access variables that belongs to the class
        :return: Nothing
        """
        self.find()
        if self.photolist is None:  # if there is no image in the given directory, show warning
            self.warning()
            return

        for images in self.photolist:
            self.entrypath = self.entry.get()
            self.imgpath = self.entrypath + "\\" + images  # create the path to the image
            self.photos_done += 1
            self.dir_path = self.get_path()  # get the path of the directories that should be created

            if self.dir_path is not None:  # if get path send something back
                self.mkdir()  # create the directories
                self.moving()  # move the image to the directories created

            # self.get_percentage(lenphotos, photos_done)

    def get_entry_path(self):
        """
        get the path and the way of sorting from the entry boxs in the window
        """

        self.vartri = self.tri_entry.get()
        self.entrypath = self.entry.get()
        self.tri()


if __name__ == "__main__":
    app = Photosorter()
    app.mainloop()
