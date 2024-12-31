import shutil
import os
import datetime
import yaml


class FileMover:

    def __init__(self, moveLocation):
        self.moveLocation = moveLocation
        if not os.path.exists(moveLocation):
            os.makedirs(moveLocation)

    def rename(self, fileName):
        nameTokens = os.path.splitext(fileName)
        # Add a separator to the new file
        newFileName = ''.join(
            [nameTokens[0], '_', nameTokens[1]])
        return newFileName

    def move(self, fileLocation):
        if not os.path.isfile(fileLocation):  # Ensure it's a file
            return
        
        fileName = os.path.basename(fileLocation)

        while os.path.isfile(os.path.join(self.moveLocation, fileName)):
            fileName = self.rename(fileName)

        try:
            print("Moving {} to {}".format(fileLocation, self.moveLocation))
            shutil.move(fileLocation, self.moveLocation)
        except Exception as e:
            print("Couldn't move {}: {}".format(fileLocation, e))


def sortbyType(path):
    srcLoc = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), '..', 'config', 'filegroups.yml')
    distLoc = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'config', 'filegroups.yml')

    filegroups = ''
    try:
        filegroups = yaml.load(
            open(srcLoc), Loader=yaml.FullLoader)
    except FileNotFoundError:
        filegroups = yaml.load(
            open(distLoc), Loader=yaml.FullLoader)

    filekeys = filegroups.keys()
    filePool = []
    for key in filekeys:
        for file in filegroups[key]:
            filePool.append(file)
    
    for file in os.listdir(path):
        currentLoc = os.path.join(path, file)

        if not os.path.isfile(currentLoc):  # Skip directories
            continue

        fileExt = os.path.splitext(file)[1].replace('.', '')
        folderName = 'Others'
        for key in filekeys:
            if fileExt.lower() in [ext.lower() for ext in filegroups[key]]:
                folderName = key
                break

        destination = os.path.join(path, folderName)
        fm = FileMover(destination)
        fm.move(currentLoc)
