import os, shutil

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

def Remove(_path):
    if os.path.isfile(_path):
        os.remove(_path)
    elif os.path.isdir(_path):
        for path_sub_name in os.listdir(_path):
            _path_sub = os.path.join(_path, path_sub_name)
            Remove(_path_sub)
        os.rmdir(_path)
    else:
        print(_path)
def Copy(src_path, dst_folder):
    path_name = os.path.basename(src_path)
    if os.path.isfile(src_path):
        dst_path = os.path.join(dst_folder, path_name)
        shutil.copy(src_path, dst_path)
    elif os.path.isdir(src_path):
        dst_folder_sub = os.path.join(dst_folder, path_name)
        os.mkdir(dst_folder_sub)
        for path_sub_name in os.listdir(src_path):
            src_path_sub = os.path.join(src_path, path_sub_name)
            Copy(src_path_sub, dst_folder_sub)
    else:
        print(src_path)
def Move(src_path, dst_folder):
    pass

if __name__ == '__main__':
    pass
