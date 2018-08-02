class DirFileHandler:

    def __init__(self):
        None

    def getIDFromPath(self, path):
        splitted = path.split("\\")
        return splitted[len(splitted)-1].split('.')[0]