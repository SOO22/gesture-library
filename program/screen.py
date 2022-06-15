from tkinter import *

from PIL import Image, ImageTk

import library as img_man


# creates the screen for the gesture drawing reference images
class GestureScreen(Frame):

    # define a function for the screen frame
    def __init__(self, parent):
        super().__init__(parent)
        self.ButtonPause = None
        self.ButtonSkip = None
        self.ButtonFinish = None
        self.LabelRemainingTime = None
        self.ButtonPrev = None
        self.ButtonExit = None
        self.bruteImg = None
        self.TKimg = None
        self.exitToMenu = None
        self.thumb = None
        self.topFrame = parent
        self.activeSession = Frame(self)
        self.slideShowSession = Frame(self)
        self.time = 0
        self.timeM = 0
        self.timeS = 0
        self.currentTime = StringVar(value="00:00")
        self.set_clock()
        self.images = 0
        self.completedImages = 0
        self.currentImage = -1
        self.imgCount = StringVar(value="0/0")
        self.isActive = False
        self.isPaused = False
        self.maxIndex = 0
        self.canceled = 0

        self.create_active_session_ui(self.activeSession)

        self.create_slide_show_session(self.slideShowSession)

        self.imgContainer = Label(self)
        self.imgContainer.place(anchor="center", relx=0.5, rely=0.5, relwidth=0.75, relheight=0.75)
        self.labelImgCounter = Label(self, textvariable=self.imgCount)
        self.labelImgCounter.place(anchor="center", relx=0.5, rely=0.05)
        self.textImgPath = Text(self, wrap="char")
        self.textImgPath.place(anchor="sw", relx=0, rely=1, relwidth=0.12, relheight=0.12)

    # defines a function for active session interaction
    def create_active_session_ui(self, parent):

        bt_placement_y = 10
        self.ButtonPause = Button(parent, text="Pause", height=2, width=8, command=self.toggle_pause, fg='silver',
                                  bg='grey9')
        self.ButtonPause.place(anchor="ne", relx=1, rely=0, x=-10, y=bt_placement_y)
        bt_placement_y += 60
        self.ButtonSkip = Button(parent, text="Skip", height=2, width=8, command=self.skip_image, fg='silver',
                                 bg='grey9')
        self.ButtonSkip.place(anchor="ne", relx=1, rely=0, x=-10, y=bt_placement_y)
        bt_placement_y = -10
        self.ButtonFinish = Button(parent, text="Finish", height=2, width=8, command=self.end_session, fg='silver',
                                   bg='grey9')
        self.ButtonFinish.place(anchor="se", relx=1, rely=1, x=-10, y=bt_placement_y)
        self.LabelRemainingTime = Label(parent, textvariable=self.currentTime, justify="left")
        self.LabelRemainingTime.place(anchor="nw", relx=0, rely=0, x=10, y=10)

    # defines a function for slideshow interaction
    def create_slide_show_session(self, parent):
        self.ButtonPrev = Button(parent, text="<<", height=2, width=5, command=self.prev_image, fg='silver', bg='grey9')
        self.ButtonPrev.place(anchor="center", relx=0.5, rely=0.05, x=-50)
        self.ButtonPrev = Button(parent, text=">>", height=2, width=5, command=self.next_image, fg='silver', bg='grey9')
        self.ButtonPrev.place(anchor="center", relx=0.5, rely=0.05, x=50)
        bt_placement_y = -10
        self.ButtonExit = Button(parent, text="Exit", height=2, width=8, command=self.exit_session, fg='silver',
                                 bg='grey9')
        self.ButtonExit.place(anchor="se", relx=1, rely=1, x=-10, y=bt_placement_y)

    # a function for the session information using conditionals
    def set_session(self, session_info):
        self.activeSession.place_forget()
        self.slideShowSession.place_forget()
        self.time = session_info[0]
        self.images = session_info[1]
        if self.images == 0 or self.images >= img_man.get_image_len():
            self.images = img_man.get_image_len()
        if self.time > 0:
            self.isActive = True
            self.isPaused = False
            self.set_clock()
            self.activeSession.place(relx=0, relheight=1, relwidth=1)
            self.start_time_loop()
            self.maxIndex = 0
        else:
            self.isActive = False
            self.slideShowSession.place(relx=0, relheight=1, relwidth=1)
            self.maxIndex = self.images - 1
        self.maxIndex = min(self.maxIndex, img_man.get_image_len() - 1)
        self.completedImages = 0
        self.currentImage = -1
        self.next_image()
        self.set_progress()

    # a function for session progress
    def set_progress(self):
        if self.isActive:
            self.imgCount.set(str(self.completedImages + 1) + "/" + str(self.images))
        else:
            self.imgCount.set(str(self.currentImage + 1))

    def set_clock(self):
        self.timeM = self.time // 60
        self.timeS = self.time % 60
        self.update_clock()

    def update_clock(self):
        s = ""
        if self.timeM < 10:
            s += "0"
        s += str(self.timeM)
        s += ":"
        if self.timeS < 10:
            s += "0"
        s += str(self.timeS)
        self.currentTime.set(s)

    def start_time_loop(self):
        self.canceled = self.activeSession.after(1000, self.reduce_second)

    def reduce_second(self):
        self.canceled = self.activeSession.after(1000, self.reduce_second)
        self.timeS -= 1
        if self.timeS < 0:
            self.timeS = 59
            self.timeM -= 1
            if self.timeM < 0:
                self.set_clock()
                self.new_image()
        self.update_clock()

    # a function to count completed images
    def new_image(self):
        self.completedImages += 1
        if self.completedImages >= self.images:
            self.end_session()
        else:
            self.add_max_index()
            self.next_image()

    def skip_image(self):
        self.add_max_index()
        self.set_clock()
        self.next_image()
        self.activeSession.after_cancel(self.canceled)
        self.start_time_loop()

    def next_image(self):
        self.currentImage += 1
        if self.currentImage > self.maxIndex:
            self.currentImage = 0
        n_image = img_man.get_image(self.currentImage)
        self.textImgPath.delete(1.0, "end")
        self.textImgPath.insert(1.0, n_image)
        self.place_image(n_image)
        self.set_progress()

    def prev_image(self):
        self.currentImage -= 1
        if self.currentImage < 0:
            self.currentImage = self.maxIndex
        p_image = img_man.get_image(self.currentImage)
        self.textImgPath.delete(1.0, "end")
        self.textImgPath.insert(1.0, p_image)
        self.place_image(p_image)
        self.set_progress()

    def end_session(self):
        self.activeSession.after_cancel(self.canceled)
        self.isActive = False
        self.activeSession.place_forget()
        self.slideShowSession.place(relx=0, relheight=1, relwidth=1)
        self.set_progress()

    def toggle_pause(self):
        self.isPaused = not self.isPaused
        if self.isPaused:
            self.activeSession.after_cancel(self.canceled)
        else:
            self.start_time_loop()

    def place_image(self, imgPath):
        self.bruteImg = Image.open(imgPath)
        self.thumb = self.bruteImg.copy()
        self.thumb.thumbnail((self.imgContainer.winfo_width(), self.imgContainer.winfo_height()), Image.ANTIALIAS)
        self.TKimg = ImageTk.PhotoImage(self.thumb)
        self.imgContainer.image = ImageTk.PhotoImage(self.thumb)
        self.imgContainer.config(image=self.imgContainer.image)
        self.imgContainer.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        self.thumb = self.bruteImg.copy()
        self.thumb.thumbnail((event.width, event.height), Image.ANTIALIAS)
        self.TKimg = ImageTk.PhotoImage(self.thumb)
        self.imgContainer.image = ImageTk.PhotoImage(self.thumb)
        self.imgContainer.config(image=self.imgContainer.image)

    def exit_session(self):
        self.exitToMenu()

    def add_max_index(self):
        self.maxIndex += 1
        self.maxIndex = min(self.maxIndex, img_man.get_image_len() - 1)

    def bind_exit_session(self, func):
        self.exitToMenu = func
