''' code for display screen '''
from tkinter import *

from PIL import Image, ImageTk

import library as imgMan


# creates the screen for the gesture drawing reference images
class GestureScreen(Frame):

    # define a function for the screen frame
    def __init__(self, parent):
        super().__init__(parent)
        self.topFrame = parent
        self.activeSession = Frame(self)
        self.slideShowSession = Frame(self)
        self.time = 0
        self.timeM = 0
        self.timeS = 0
        self.currentTime = StringVar(value="00:00")
        self.setClock()
        self.images = 0
        self.completedImages = 0
        self.currentImage = -1
        self.imgCount = StringVar(value="0/0")
        self.isActive = False
        self.isPaused = False
        self.maxIndex = 0
        self.cancelid = 0

        self.createActiveSessionUI(self.activeSession)

        self.createSlideShowSession(self.slideShowSession)

        self.imgContainer = Label(self)
        self.imgContainer.place(anchor="center", relx=0.5, rely=0.5, relwidth=0.75, relheight=0.75)
        self.labelImgCounter = Label(self, textvariable=self.imgCount)
        self.labelImgCounter.place(anchor="center", relx=0.5, rely=0.05)
        self.textImgPath = Text(self, wrap="char")
        self.textImgPath.place(anchor="sw", relx=0, rely=1, relwidth=0.12, relheight=0.12)

    # defines a function for active session interaction
    def createActiveSessionUI(self, parent):

        btPlacementy = 10
        self.ButtonPause = Button(parent, text="Pause", height=2, width=8, command=self.togglePause, fg='silver',
                                  bg='grey9')
        self.ButtonPause.place(anchor="ne", relx=1, rely=0, x=-10, y=btPlacementy)
        btPlacementy += 60
        self.ButtonSkip = Button(parent, text="Skip", height=2, width=8, command=self.skipImage, fg='silver',
                                 bg='grey9')
        self.ButtonSkip.place(anchor="ne", relx=1, rely=0, x=-10, y=btPlacementy)
        btPlacementy = -10
        self.ButtonFinish = Button(parent, text="Finish", height=2, width=8, command=self.endSession, fg='silver',
                                   bg='grey9')
        self.ButtonFinish.place(anchor="se", relx=1, rely=1, x=-10, y=btPlacementy)
        self.LabelRemainingTime = Label(parent, textvariable=self.currentTime, justify="left")
        self.LabelRemainingTime.place(anchor="nw", relx=0, rely=0, x=10, y=10)

    # defines a function for slideshow interaction
    def createSlideShowSession(self, parent):
        self.ButtonPrev = Button(parent, text="<<", height=2, width=5, command=self.prevImage, fg='silver', bg='grey9')
        self.ButtonPrev.place(anchor="center", relx=0.5, rely=0.05, x=-50)
        self.ButtonPrev = Button(parent, text=">>", height=2, width=5, command=self.nextImage, fg='silver', bg='grey9')
        self.ButtonPrev.place(anchor="center", relx=0.5, rely=0.05, x=50)
        btPlacementy = -10
        self.ButtonExit = Button(parent, text="Exit", height=2, width=8, command=self.exitSession, fg='silver',
                                 bg='grey9')
        self.ButtonExit.place(anchor="se", relx=1, rely=1, x=-10, y=btPlacementy)

    # a function for the session information using conditionals
    def setSession(self, sessionInfo):
        self.activeSession.place_forget()
        self.slideShowSession.place_forget()
        self.time = sessionInfo[0]
        self.images = sessionInfo[1]
        if (self.images == 0 or self.images >= imgMan.getImageLen()):
            self.images = imgMan.getImageLen()
        if (self.time > 0):
            self.isActive = True
            self.isPaused = False
            self.setClock()
            self.activeSession.place(relx=0, relheight=1, relwidth=1)
            self.startTimeLoop()
            self.maxIndex = 0
        else:
            self.isActive = False
            self.slideShowSession.place(relx=0, relheight=1, relwidth=1)
            self.maxIndex = self.images - 1
        self.maxIndex = min(self.maxIndex, imgMan.getImageLen() - 1)
        self.completedImages = 0
        self.currentImage = -1
        self.nextImage()
        self.setProgress()

    # a function for session progress
    def setProgress(self):
        if (self.isActive):
            self.imgCount.set(str(self.completedImages + 1) + "/" + str(self.images))
        else:
            self.imgCount.set(str(self.currentImage + 1))

    def setClock(self):
        self.timeM = self.time // 60
        self.timeS = self.time % 60
        self.updateClock()

    def updateClock(self):
        s = ""
        if (self.timeM < 10):
            s += "0"
        s += str(self.timeM)
        s += ":"
        if (self.timeS < 10):
            s += "0"
        s += str(self.timeS)
        self.currentTime.set(s)

    def startTimeLoop(self):
        self.cancelid = self.activeSession.after(1000, self.reduceSecond)

    def reduceSecond(self):
        self.cancelid = self.activeSession.after(1000, self.reduceSecond)
        self.timeS -= 1
        if (self.timeS < 0):
            self.timeS = 59
            self.timeM -= 1
            if (self.timeM < 0):
                self.setClock()
                self.newImage()
        self.updateClock()

    # a function to count completed images
    def newImage(self):
        self.completedImages += 1
        if (self.completedImages >= self.images):
            self.endSession()
        else:
            self.addMaxIndex()
            self.nextImage()

    def skipImage(self):
        self.addMaxIndex()
        self.setClock()
        self.nextImage()
        self.activeSession.after_cancel(self.cancelid)
        self.startTimeLoop()

    def nextImage(self):
        self.currentImage += 1
        if (self.currentImage > self.maxIndex): self.currentImage = 0
        nImage = imgMan.getImage(self.currentImage)
        self.textImgPath.delete(1.0, "end")
        self.textImgPath.insert(1.0, nImage)
        self.placeImage(nImage)
        self.setProgress()

    def prevImage(self):
        self.currentImage -= 1
        if (self.currentImage < 0): self.currentImage = self.maxIndex
        pImage = imgMan.getImage(self.currentImage)
        self.textImgPath.delete(1.0, "end")
        self.textImgPath.insert(1.0, pImage)
        self.placeImage(pImage)
        self.setProgress()

    def endSession(self):
        self.activeSession.after_cancel(self.cancelid)
        self.isActive = False
        self.activeSession.place_forget()
        self.slideShowSession.place(relx=0, relheight=1, relwidth=1)
        self.setProgress()

    def togglePause(self):
        self.isPaused = not self.isPaused
        if (self.isPaused):
            self.activeSession.after_cancel(self.cancelid)
        else:
            self.startTimeLoop()

    def placeImage(self, imgPath):
        self.bruteImg = Image.open(imgPath)
        self.thumb = self.bruteImg.copy()
        self.thumb.thumbnail((self.imgContainer.winfo_width(), self.imgContainer.winfo_height()), Image.ANTIALIAS)
        self.TKimg = ImageTk.PhotoImage(self.thumb)
        self.imgContainer.image = ImageTk.PhotoImage(self.thumb)
        self.imgContainer.config(image=self.imgContainer.image)
        self.imgContainer.bind("<Configure>", self.resizeImage)

    def resizeImage(self, event):
        self.thumb = self.bruteImg.copy()
        self.thumb.thumbnail((event.width, event.height), Image.ANTIALIAS)
        self.TKimg = ImageTk.PhotoImage(self.thumb)
        self.imgContainer.image = ImageTk.PhotoImage(self.thumb)
        self.imgContainer.config(image=self.imgContainer.image)

    def exitSession(self):
        self.exitToMenu()

    def addMaxIndex(self):
        self.maxIndex += 1
        self.maxIndex = min(self.maxIndex, imgMan.getImageLen() - 1)

    def bindExitSession(self, func):
        self.exitToMenu = func
