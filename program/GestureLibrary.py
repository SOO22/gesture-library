''' code for main program '''

from tkinter import *

import library as imgMan
from menu import MainMenu
from screen import GestureScreen


# defines a function to sart the session using a conditional
def startSession(tu):
    if (imgMan.getImageLen() > 0):
        imgMan.randomizeImages()
        mainMenu.place_forget()

        gestureScreen.setSession(tu)
        gestureScreen.place(relx=0, relheight=1, relwidth=1)


# defines a function to exit the session using a conditional
def exitSession():
    if (imgMan.getImageLen() > 0):
        gestureScreen.place_forget()
        mainMenu.place(relx=0, relheight=1, relwidth=1)


# creates the main program window
root = Tk()
root.iconphoto = ("")  # assigns the window logo
root.title("GestureLibrary")  # assigns the window title
root.geometry("800x600")  # sets the window width and height

# Add a Canvas widget
topFrame = Frame(root)
imgMan.loadFolders()

topFrame.place(relx=0, relheight=1, relwidth=1)
mainMenu = MainMenu(topFrame)
mainMenu.place(relx=0, relheight=1, relwidth=1)
mainMenu.setFolders()

mainMenu.bindStartSession(startSession)
gestureScreen = GestureScreen(topFrame)
gestureScreen.bindExitSession(exitSession)

root.mainloop()  # calls the mainloop() function
