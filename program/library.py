import os
import random

dirList = []
allImages = []
validImageExtensions = ("jpg", "jpeg", "png", "gif")


def update_image_count(selected):
    """updates the total number of images counted"""
    global allImages
    allImages = []
    total_images = 0

    for folderIndex, folderEnabled in enumerate(selected):
        if folderEnabled:
            p = dirList[folderIndex]
            list_dir = os.listdir(p)

            for fileIndex, file in enumerate(list_dir):
                file_path = "./" + p + "/" + file

                if os.path.isfile(file_path):
                    if valid_image_file(file):
                        total_images += 1
                        allImages.append((folderIndex, fileIndex))

    return str(total_images)


def get_image(index=0):
    """gets the images from the specified folder"""
    image_path = "null"
    if index < len(allImages):
        folder_index = allImages[index][0]
        folder_name = dirList[folder_index]
        image_index = allImages[index][1]
        image_name = os.listdir(folder_name)[image_index]
        image_path = "./" + folder_name + "/" + image_name
    return image_path


def valid_image_file(file_name):
    extension = file_name.split(".")[-1].lower()
    return extension in validImageExtensions


def load_folders():
    global dirList
    dirList = []
    list_dir = os.listdir()
    for file in list_dir:
        if os.path.isdir(file):
            dirList.append(file)


def get_image_len():
    return len(allImages)


def randomize_images():
    global allImages
    random.shuffle(allImages)
    pass
