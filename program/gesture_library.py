from tkinter import *

import library as img_man
from menu import MainMenu
from screen import GestureScreen


def start_session(tu):
    """start a drawing session"""
    if img_man.get_image_len() > 0:
        img_man.randomize_images()
        mainMenu.place_forget()

        gestureScreen.set_session(tu)
        gestureScreen.place(relx=0, relheight=1, relwidth=1)


def exit_session():
    """exits the drawing session"""
    if img_man.get_image_len() > 0:
        gestureScreen.place_forget()
        mainMenu.place(relx=0, relheight=1, relwidth=1)


# creates the main program window
root = Tk()
root.iconphoto = ""  # assigns the window logo
root.title("GestureLibrary")  # assigns the window title
root.geometry("800x600")  # sets the window width and height

# Add a Canvas widget
topFrame = Frame(root)
img_man.load_folders()

topFrame.place(relx=0, relheight=1, relwidth=1)
mainMenu = MainMenu(topFrame)
mainMenu.place(relx=0, relheight=1, relwidth=1)
mainMenu.set_folders()

mainMenu.bind_start_session(start_session)
gestureScreen = GestureScreen(topFrame)
gestureScreen.bind_exit_session(exit_session)

root.mainloop()
