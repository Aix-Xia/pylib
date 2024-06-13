import os

def GetFileName(filePath, suffix=False):
    """
    获取文件名
    :param filePath: 文件地址
    :param suffix: 是否带文件拓展名
    :return: 文件名
    """
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
    """
    获取文件拓展名
    :param filePath:文件地址
    :return: 文件拓展名
    """
    if os.path.isfile(filePath):
        fileName = os.path.basename(filePath)
        ip = fileName.rfind('.')
        return fileName[ip+1:]
    elif filePath.find('\\') == -1 and filePath.find('/') == -1:
        ip = filePath.rfind('.')
        return filePath[ip+1:]
    else:
        raise (ValueError(f'"{filePath}" is not file!'))

def GetSize(path):
    """
    获取文件或者文件夹占用内存大小
    :param path: 文件或者文件夹地址
    :return: 文件或者文件夹占用内存大小
    """
    size = 0
    if os.path.isfile(path):
        size += os.path.getsize(path)
    elif os.path.isdir(path):
        for name in os.listdir(path):
            subPath = os.path.join(path, name)
            size += GetSize(subPath)
    return size

def GetFileCount(_path):
    """
    获取文件夹及其子文件夹中的所有文件个数
    :param _path: 文件夹地址
    :return: 文件个数
    """
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
    """
    删除文件或者文件夹（包含文件夹中的所有内容）
    :param _path: 文件或者文件夹地址
    :return:
    """
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
    """
    删除文件或者文件夹（包含文件夹中的所有内容）
    :param args: 多个 文件或者文件夹地址
    :return: None
    """
    for _path in args:
        RemovePath(_path)

def LoopFile(_path, recursion=True):
    """
    迭代输出文件夹中的文件地址，
    :param _path: 文件夹地址
    :param recursion: 递归，True：递归子文件夹中的文件；False：只输出_path地址下的文件
    :return: 文件地址
    """
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