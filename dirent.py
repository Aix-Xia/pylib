import os

def GetFileName(filePath, suffix=False):
    if os.path.isfile(filePath):
        fileName = os.path.basename(filePath)
        ip = fileName.rfind('.')
        return fileName if suffix else fileName[:ip]
    elif filePath.find('\\') == -1 and filePath.find('/') == -1:
        ip = filePath.rfind('.')
        return filePath if suffix else filePath[:ip]
    else:
        raise(ValueError(f'"{filePath}" is not file!'))

def GetFileType(filePath):
    if os.path.isfile(filePath):
        fileName = os.path.basename(filePath)
        ip = fileName.rfind('.')
        return fileName[ip+1:]
    elif filePath.find('\\') == -1 and filePath.find('/') == -1:
        ip = filePath.rfind('.')
        return filePath[ip+1:]
    else:
        raise (ValueError(f'"{filePath}" is not file!'))

def GetFileCount(_path):
    counter = 0
    for itemName in os.listdir(_path):
        item = os.path.join(_path, itemName)
        if os.path.isfile(item):
            counter += 1
        elif os.path.isdir(item):
            counter += GetFileCount(item)
        else:
            raise(NotADirectoryError('pls check!'))
    return counter

def RemovePath(_path):
    if os.path.isdir(_path):
        for item in os.listdir(_path):
            item = os.path.join(_path, item)
            RemovePath(item)
        os.rmdir(_path)
    elif os.path.isfile(_path):
        os.remove(_path)
    else:
        pass

def RemovePaths(*args):
    for _path in args:
        RemovePath(_path)

def LoopFile(_path, recursion=True):
    lst = os.listdir(_path)
    for itemName in lst:
        item = os.path.join(_path, itemName)
        if os.path.isdir(item):
            if recursion:
                for file in LoopFile(item):
                    yield file
        elif os.path.isfile(item):
            yield item
        else:
            pass


if __name__ == '__main__':
    pass