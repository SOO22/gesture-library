''' code for managing images library '''
import os
import random

dirList = []
allImages = []
validImageExtensions = ("jpg", "jpeg", "png", "gif")


# defines the function for updating the image count
def updateImageCount(selected):
    # access all images
    global allImages
    allImages = []
    # currentImages=0
    totalImages = 0
    # totalFiles=0

    # using conditionals to iterate through folders
    for folderIndex, folderEnabled in enumerate(selected):
        if (folderEnabled):
            # currentImages=0
            p = dirList[folderIndex]
            list = os.listdir(p)

            for fileIndex, file in enumerate(list):
                filePath = "./" + p + "/" + file

                if (os.path.isfile(filePath)):
                    if (validImageFile(file)):
                        totalImages += 1
                        allImages.append((folderIndex, fileIndex))

    # returns total images as a string
    return str(totalImages)


# defines the function for getting the images in the folder
def getImage(index=0):
    imagePath = "null"
    if (index < len(allImages)):
        folderIndex = allImages[index][0]
        folderName = dirList[folderIndex]
        imageIndex = allImages[index][1]
        imageName = os.listdir(folderName)[imageIndex]
        imagePath = "./" + folderName + "/" + imageName
    return imagePath


def validImageFile(fileName):
    extension = fileName.split(".")[-1].lower()
    return extension in validImageExtensions


def loadFolders():
    global dirList
    dirList = []
    list = os.listdir()
    for file in list:
        if (os.path.isdir(file)):
            dirList.append(file)


def getImageLen():
    return len(allImages)


def randomizeImages():
    global allImages
    random.shuffle(allImages)
    pass
