import sys
import time
import os
from pylib import checker

class RECORDER:
    _instance = None
    _create = False
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if not RECORDER._create:
            self.lenStr = 100
            self.header = 'start'
            self.tailer = 'end'
            self.fillChar = '*'
            self.folderRecord = os.path.join(os.getcwd(), 'Record')
            self.fileNamePrint = r'funcPrint'
            self.fileNameCallFunc = r'CallFunc'
            self.fileNameLog = r'datalog'
            RECORDER._create = True
    def __lenStr_set(self, _value):
        if checker.NaturalNumber(_value, False):
            self.__lenStr = _value
    lenStr = property(lambda self:self.__lenStr, __lenStr_set, lambda self:None, 'This is lenStr!')
    def __header_set(self, _value):
        if type(_value) != str:
            _value = str(_value)
        self.__header = _value
    header = property(lambda self:self.__header, __header_set, lambda self:None, 'This is header!')
    def __tailer_set(self, _value):
        if type(_value) != str:
            _value = str(_value)
        self.__tailer = _value
    tailer = property(lambda self:self.__tailer, __tailer_set, lambda self:None, 'This is tailer!')
    def __fillChar_set(self, _value):
        if checker.Char(_value):
            self.__fillChar = _value
    fillChar = property(lambda self:self.__fillChar, __fillChar_set, lambda self:None, 'This is fillChar!')
    def __folderRecord_set(self, _path):
        if os.path.isfile(_path):
            print(f'{_path} is not folder, change folder is fail!')
        elif not os.path.isdir(_path):
            os.mkdir(_path)
            self.__folderRecord = _path
        else:
            self.__folderRecord = _path
    folderRecord = property(lambda self:self.__folderRecord, __folderRecord_set, lambda self:None, 'This is folderRecord!')
    def __fileNamePrint_set(self, _fileName):
        if not checker.NamingRule(_fileName):
            print(f'{_fileName} do not match naming rule! change print file name fail!')
        else:
            self.__fileNamePrint = _fileName
    fileNamePrint = property(lambda self:self.__fileNamePrint, __fileNamePrint_set, lambda self:None, 'This is fileNamePrint')
    def __fileNameCallFunc_set(self, _fileName):
        if not checker.NamingRule(_fileName):
            print(f'{_fileName} do not match naming rule! change call func file name fail!')
        else:
            self.__fileNameCallFunc = _fileName
    fileNameCallFunc = property(lambda self:self.__fileNameCallFunc, __fileNameCallFunc_set, lambda self:None, 'This is fileNameCallFunc')
    def __fileNameLog_set(self, _fileName):
        if not checker.NamingRule(_fileName):
            print(f'{_fileName} do not match naming rule! change log file name fail!')
        else:
            self.__fileNameLog = _fileName
    fileNameLog = property(lambda self:self.__fileNameLog, __fileNameLog_set, lambda self:None, 'This is fileNameLog')
    @property
    def filePrint(self):
        return os.path.join(self.folderRecord, self.fileNamePrint + '.dat')
    @property
    def fileCallFunc(self):
        return os.path.join(self.folderRecord, self.fileNameCallFunc + '.dat')
    @property
    def fileLog(self):
        return os.path.join(self.folderRecord, self.fileNameLog + '.dat')
record = RECORDER()

def SetRecorder(**kwargs):
    record.lenStr = kwargs.get('lenStr', record.lenStr)
    record.header = kwargs.get('header', record.header)
    record.tailer = kwargs.get('tailer', record.tailer)
    record.fillChar = kwargs.get('fillChar', record.fillChar)
    record.folderRecord = kwargs.get('folderRecord', record.folderRecord)
    record.fileNamePrint = kwargs.get('fileNamePrint', record.fileNamePrint)
    record.fileNameCallFunc = kwargs.get('fileNameCallFunc', record.fileNameCallFunc)
    record.fileNameLog = kwargs.get('fileNameLog', record.fileNameLog)

def RecordCallFunc(func):
    """
    装饰器 --- 在指定文件中记录函数被调用情况
    """
    def run(*args, **kwargs):
        localTime = time.localtime()
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        with open(record.fileCallFunc, 'a+', encoding='utf-8', newline='') as fw:
            fw.write(f'[Record][{func.__name__}][{localTime.tm_year}-{localTime.tm_mon}-{localTime.tm_mday} {localTime.tm_hour}:{localTime.tm_min}:{localTime.tm_sec}] has used {1000*(t1-t0)}ms\n')
        return result
    return run

def RecordPrint(func):
    """
    装饰器 --- 函数中的print全部打印到指定文件中
    """
    def run(*args, **kwargs):
        with open(record.filePrint, 'a+', encoding='utf-8', newline='') as fw:
            localTime = time.localtime()
            default_stdout = sys.stdout
            sys.stdout = fw
            print(record.header.center(record.lenStr, record.fillChar))
            print(f'[{func.__name__}][RunTime]: {localTime.tm_year}-{localTime.tm_mon}-{localTime.tm_mday} {localTime.tm_hour}:{localTime.tm_min}:{localTime.tm_sec}')
            t0 = time.time()
            result = func(*args, **kwargs)
            t1 = time.time()
            print(f'[{func.__name__}][UserTime]: {1000*(t1-t0)}ms')
            print(record.tailer.center(record.lenStr, record.fillChar))
            sys.stdout = default_stdout
        return result
    return run

def RecordLog(*args, **kwargs):
    """
    将需要记录的内容记录到指定文件，用法与print()相似
    :param args: 打印内容
    :param kwargs: 打印设置
    """
    lst = list(map(lambda i:str(i), args))
    fw = open(record.fileLog, 'a+', encoding='utf-8', newline='')
    sep = kwargs.get('sep', None)
    end = kwargs.get('end', None)
    file = kwargs.get('file', fw)
    flush = kwargs.get('flush', None)
    print(*lst, sep=sep, end=end, file=file, flush=flush)
    if not fw.closed:
        fw.close()



if __name__ == '__main__':
    pass