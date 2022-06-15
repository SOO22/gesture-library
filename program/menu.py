from tkinter import *

import library as img_man


# the class groups all the contents of the program menu
class MainMenu(Frame):

    # defines a function for available images and start button using the __init__ method
    def __init__(self, parent):
        super().__init__(parent)
        self.foldersContainer = None
        self.canvasScrollBar = None
        self.folderCanvas = None
        self.foldersList = None
        self.menuTime = None
        self.menuTimeTxt = None
        self.labelTime = None
        self.bt300 = None
        self.bt600 = None
        self.entryTime = None
        self.menuImages = None
        self.menuImagesTxt = None
        self.labelImages = None
        self.bt00 = None
        self.bt15 = None
        self.bt30 = None
        self.bt45 = None
        self.bt60 = None
        self.bt90 = None
        self.bt120 = None
        self.bt_custom = None
        self.entryImages = None
        self.btca = None
        self.setSession = None
        self.passFolders = None
        self.topFrame = parent
        self.configure(bg='grey12')

        f1 = Frame(self, height=300, bg="grey9")
        f1.pack(fill=BOTH)

        self.label = Label(parent, text="Gesture Library", fg='silver', bg='grey9', font=("Helvetica", 40))
        self.label.place(anchor="center", relx=0.5, rely=0.5, y=-200)
        self.time = 0
        self.images = 0
        self.foldersSelected = []
        self.create_folder_list(self)
        self.create_time_selection(self)
        self.create_image_selection(self)
        self.available = StringVar(value="Total Images Available: 0")
        self.labelTotalImages = Label(self, textvariable=self.available, fg='silver', bg='grey12')
        self.labelTotalImages.place(anchor="n", relx=0.5, rely=0.5, y=-160)
        self.btStart = Button(self, text="Draw", height=3, width=15, command=self.prepare_session, fg='silver',
                              bg='grey12')
        self.btStart.place(anchor="center", relx=0.5, rely=0.5, y=250)

    # defines a function  to create and contain the image folders and a vertical scrolling option
    def create_folder_list(self, parent):
        self.foldersContainer = LabelFrame(parent, text="Folders", fg='silver', bg='grey12')
        self.foldersContainer.place(anchor="center", relx=0.5, rely=0.5, relheight=.2, relwidth=.5, y=-70, x=0)
        self.canvasScrollBar = Scrollbar(self.foldersContainer, orient="vertical")
        self.canvasScrollBar.pack(side="right", fill="y")
        self.canvasScrollBar.bind("<Configure>", self.update_scroll_bar)
        self.folderCanvas = Canvas(self.foldersContainer, yscrollcommand=self.canvasScrollBar.set)
        self.canvasScrollBar.configure(command=self.folderCanvas.yview)
        self.foldersList = Frame(self.folderCanvas)
        self.folderCanvas.create_window(0, 0, window=self.foldersList, anchor="nw")
        self.folderCanvas.pack(fill='both')

    # defines a function to create radio buttons for drawing times per image
    def create_time_selection(self, parent):
        self.menuTime = IntVar(value=30)
        self.menuTimeTxt = StringVar(value="30")
        bt_placement_y = 60
        self.labelTime = Label(parent, text="Select a fixed time for all images:", height=3, fg='grey', bg='grey12')
        self.labelTime.place(anchor="n", relx=0.5, rely=0.5, y=bt_placement_y)
        self.bt00 = Radiobutton(parent, text="Unlimited", variable=self.menuTime, value=0, command=self.select_time,
                                fg='grey', bg='grey12')
        bt_placement_y += 50
        self.bt00.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=-240)
        self.bt30 = Radiobutton(parent, text="30s", variable=self.menuTime, value=30, command=self.select_time,
                                fg='grey', bg='grey12')
        self.bt30.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=-180)
        self.bt45 = Radiobutton(parent, text="45s", variable=self.menuTime, value=45, command=self.select_time,
                                fg='grey', bg='grey12')
        self.bt45.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=-120)
        self.bt60 = Radiobutton(parent, text="1m", variable=self.menuTime, value=60, command=self.select_time, fg='grey',
                                bg='grey12')
        self.bt60.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=-60)
        self.bt120 = Radiobutton(parent, text="2m", variable=self.menuTime, value=120, command=self.select_time,
                                 fg='grey', bg='grey12')
        self.bt120.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=0)
        self.bt300 = Radiobutton(parent, text="5m", variable=self.menuTime, value=300, command=self.select_time,
                                 fg='grey', bg='grey12')
        self.bt300.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=60)
        self.bt600 = Radiobutton(parent, text="10m", variable=self.menuTime, value=600, command=self.select_time,
                                 fg='grey', bg='grey12')
        self.bt600.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=120)
        self.bt_custom = Radiobutton(parent, text="Custom", variable=self.menuTime, value=-1, command=self.select_time,
                                     fg='grey', bg='grey12')
        self.bt_custom.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=180)
        self.entryTime = Entry(parent, width=6, textvariable=self.menuTimeTxt)
        self.entryTime.config(state=DISABLED)
        self.entryTime.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=240)

    # defines a function to create radio buttons for amount of images in a single session
    def create_image_selection(self, parent):
        self.menuImages = IntVar(value=20)
        self.menuImagesTxt = StringVar(value="20")
        self.labelImages = Label(parent, text="Select the Number of images:", height=3, fg='grey', bg='grey12')
        bt_placement_y = 130
        self.labelImages.place(anchor="n", relx=0.5, rely=0.5, y=bt_placement_y)
        bt_placement_y += 60
        self.bt00 = Radiobutton(parent, text="Max", variable=self.menuImages, value=0, command=self.select_images,
                                fg='grey', bg='grey12')
        self.bt00.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=-240)
        self.bt15 = Radiobutton(parent, text="5", variable=self.menuImages, value=5, command=self.select_images,
                                fg='grey', bg='grey12')
        self.bt15.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=-180)
        self.bt30 = Radiobutton(parent, text="10", variable=self.menuImages, value=10, command=self.select_images,
                                fg='grey', bg='grey12')
        self.bt30.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=-120)
        self.bt45 = Radiobutton(parent, text="15", variable=self.menuImages, value=15, command=self.select_images,
                                fg='grey', bg='grey12')
        self.bt45.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=-60)
        self.bt60 = Radiobutton(parent, text="20", variable=self.menuImages, value=20, command=self.select_images,
                                fg='grey', bg='grey12')
        self.bt60.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=0)
        self.bt90 = Radiobutton(parent, text="30", variable=self.menuImages, value=30, command=self.select_images,
                                fg='grey', bg='grey12')
        self.bt90.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=60)
        self.bt120 = Radiobutton(parent, text="40", variable=self.menuImages, value=40, command=self.select_images,
                                 fg='grey', bg='grey12')
        self.bt120.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=120)
        self.bt_custom = Radiobutton(parent, text="Custom", variable=self.menuImages, value=-1,
                                     command=self.select_images, fg='grey', bg='grey12')
        self.bt_custom.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=180)
        self.entryImages = Entry(parent, width=6, textvariable=self.menuImagesTxt)
        self.entryImages.config(state=DISABLED)
        self.entryImages.place(anchor="center", relx=0.5, rely=0.5, y=bt_placement_y, x=240)

    # defines a function using a method to select the images folders
    def set_folders(self):
        for dir in img_man.dirList:
            var = BooleanVar()
            self.foldersSelected.append(var)
            self.btca = Checkbutton(self.foldersList, text=dir, variable=var, command=self.get_folders)
            self.btca.pack(side="top", anchor="nw")

    # defines a function using a method to get the images in the selected folder
    def get_folders(self):
        new_list = []
        for b in self.foldersSelected:
            new_list.append(b.get())

        self.available.set("Total Images Available: " + img_man.update_image_count(new_list))

    # defines a function using a method and a conditional to get the time selected for images
    def select_time(self):
        self.time = self.menuTime.get()
        if self.time > -1:
            self.menuTimeTxt.set(self.time)
            self.entryTime.config(state=DISABLED)
        else:
            self.entryTime.config(state=NORMAL)

    # defines a function using a method to and a conditional to check for images selected
    def select_images(self):
        self.images = self.menuImages.get()
        if self.images > -1:
            self.menuImagesTxt.set(self.images)
            self.entryImages.config(state=DISABLED)
            pass
        else:
            self.entryImages.config(state=NORMAL)
            pass

    # defines a function using a method to update the scrollbar
    def update_scroll_bar(self, event):
        self.folderCanvas.configure(scrollregion=self.folderCanvas.bbox("all"))

    # defines a function using a method and a conditional to get the time/images and set the draing session
    def prepare_session(self):
        self.topFrame
        valid = False
        valid = self.validate_number(self.menuTime, self.menuTimeTxt) and \
                self.validate_number(self.menuImages, self.menuImagesTxt)
        if valid:
            self.images = self.menuImages.get()
            self.time = self.menuTime.get()
            session_options = (self.time, self.images)
            self.setSession(session_options)
        pass

    def validate_number(self, var_i, var_s):
        s = var_s.get()
        if s.isnumeric():
            var_i.set(int(s))
            return True

        else:
            var_s.set("error")
            var_i.set(-1)
            return False

    def bind_start_session(self, func):
        self.setSession = func

    def bind_update_image_count(self, func):
        self.passFolders = func
