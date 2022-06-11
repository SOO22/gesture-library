from tkinter import *

import library as imgMan
from menu import MainMenu
from screen import GestureScreen


# defines a function to start the session using a conditional
def start_session(tu):
    if imgMan.get_image_len() > 0:
        imgMan.randomize_images()
        mainMenu.place_forget()

        gestureScreen.setSession(tu)
        gestureScreen.place(relx=0, relheight=1, relwidth=1)


# defines a function to exit the session using a conditional
def exit_session():
    if imgMan.get_image_len() > 0:
        gestureScreen.place_forget()
        mainMenu.place(relx=0, relheight=1, relwidth=1)


# creates the main program window
root = Tk()
root.iconphoto = ""  # assigns the window logo
root.title("GestureLibrary")  # assigns the window title
root.geometry("800x600")  # sets the window width and height

# Add a Canvas widget
topFrame = Frame(root)
imgMan.load_folders()

topFrame.place(relx=0, relheight=1, relwidth=1)
mainMenu = MainMenu(topFrame)
mainMenu.place(relx=0, relheight=1, relwidth=1)
mainMenu.setFolders()

mainMenu.bindStartSession(start_session)
gestureScreen = GestureScreen(topFrame)
gestureScreen.bindExitSession(exit_session)

root.mainloop()  # calls the mainloop() function
