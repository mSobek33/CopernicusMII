import os, fnmatch

class FileFinder:
    def __init__(self):
        None

    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            #print(dirs)
            if name in dirs:
                print(name)
                return os.path.join(root, name)

    def find_all(self, name, path):
        result = []
        for root, dirs, files in os.walk(path):
            if name in files or name in dirs:
                result.append(os.path.join(root, name))
        return result

    def findPattern(self, pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in dirs:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result