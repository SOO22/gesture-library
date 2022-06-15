from tkinter import *

import library as img_man
from menu import MainMenu
from screen import GestureScreen


# defines a function to start the session using a conditional
def start_session(tu):
    if img_man.get_image_len() > 0:
        img_man.randomize_images()
        mainMenu.place_forget()

        gestureScreen.set_session(tu)
        gestureScreen.place(relx=0, relheight=1, relwidth=1)


# defines a function to exit the session using a conditional
def exit_session():
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
mainMenu.setFolders()

mainMenu.bindStartSession(start_session)
gestureScreen = GestureScreen(topFrame)
gestureScreen.bind_exit_session(exit_session)

root.mainloop()  # calls the mainloop() function
