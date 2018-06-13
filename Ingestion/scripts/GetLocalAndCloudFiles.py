import os, fnmatch

def find(name, path):
    for root, dirs, files in os.walk(path):
        #print(dirs)
        if name in dirs:
            print(name)
            return os.path.join(root, name)

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def findPattern(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

print(findPattern('*.SAFE', 'W:'))