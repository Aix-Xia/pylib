import sys
import time
import os
import check

class config:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        self.lenStr = 100
        self.header = 'start'
        self.tailer = 'end'
        self.fillChar = '*'
        self.folderRecord = os.path.join(os.getcwd(), 'Record')
        self.fileNamePrint = r'funcPrint'
        self.fileNameCallFunc = r'CallFunc'
        self.fileNameLog = r'datalog'
    def _lenStr_get(self):
        return self._lenStr
    def _lenStr_set(self, _value):
        if check.NaturalNumber(_value, False):
            self._lenStr = _value
    def _lenStr_del(self):
        print('lenStr has delete!')
    lenStr = property(_lenStr_get, _lenStr_set, _lenStr_del, 'This is lenStr!')
    def _header_get(self):
        return self._header
    def _header_set(self, _value):
        if type(_value) != str:
            _value = str(_value)
        self._header = _value
    def _header_del(self):
        print('header has delete!')
    header = property(_header_get, _header_set, _header_del, 'This is header!')
    def _tailer_get(self):
        return self._tailer
    def _tailer_set(self, _value):
        if type(_value) != str:
            _value = str(_value)
        self._tailer = _value
    def _tailer_del(self):
        print('tailer has delete!')
    tailer = property(_tailer_get, _tailer_set, _tailer_del, 'This is tailer!')
    def _fillChar_get(self):
        return self._fillChar
    def _fillChar_set(self, _value):
        if check.Char(_value):
            self._fillChar = _value
    def _fillChar_del(self):
        print('fillChar has delete!')
    fillChar = property(_fillChar_get, _fillChar_set, _fillChar_del, 'This is fillChar!')
    def _folderRecord_get(self):
        return self._folderRecord
    def _folderRecord_set(self, _path):
        if os.path.isfile(_path):
            _path = self._folderRecord
        elif not os.path.isdir(_path):
            os.mkdir(_path)
        self._folderRecord = _path
    def _folderRecord_del(self):
        print('folderRecord has delete!')
    folderRecord = property(_folderRecord_get, _folderRecord_set, _folderRecord_del, 'This is folderRecord!')
    def _fileNamePrint_get(self):
        return self._fileNamePrint
    def _fileNamePrint_set(self, _fileName):
        if not check.NamingRule(_fileName):
            _fileName = self._fileNamePrint
        self._fileNamePrint = _fileName
    def _fileNamePrint_del(self):
        print('fileNamePrint has delete!')
    fileNamePrint = property(_fileNamePrint_get, _fileNamePrint_set, _fileNamePrint_del, 'This is fileNamePrint')
    def _fileNameCallFunc_get(self):
        return self._fileNameCallFunc
    def _fileNameCallFunc_set(self, _fileName):
        if not check.NamingRule(_fileName):
            _fileName = self._fileNameCallFunc
        self._fileNameCallFunc = _fileName
    def _fileNameCallFunc_del(self):
        print('fileNameCallFunc has delete!')
    fileNameCallFunc = property(_fileNameCallFunc_get, _fileNameCallFunc_set, _fileNameCallFunc_del, 'This is fileNameCallFunc')
    def _fileNameLog_get(self):
        return self._fileNameLog
    def _fileNameLog_set(self, _fileName):
        if not check.NamingRule(_fileName):
            _fileName = self._fileNameLog
        self._fileNameLog = _fileName
    def _fileNameLog_del(self):
        print('fileNameLog has delete!')
    fileNameLog = property(_fileNameLog_get, _fileNameLog_set, _fileNameLog_del, 'This is fileNameLog')
    @property
    def filePrint(self):
        return os.path.join(self.folderRecord, self.fileNamePrint + '.dat')
    @property
    def fileCallFunc(self):
        return os.path.join(self.folderRecord, self.fileNameCallFunc + '.dat')
    @property
    def fileLog(self):
        return os.path.join(self.folderRecord, self.fileNameLog + '.dat')
recordConfig = config()

def SetRecordConfig(**kwargs):
    recordConfig.lenStr = kwargs.get('lenStr', recordConfig.lenStr)
    recordConfig.header = kwargs.get('header', recordConfig.header)
    recordConfig.tailer = kwargs.get('tailer', recordConfig.tailer)
    recordConfig.fillChar = kwargs.get('fillChar', recordConfig.fillChar)
    recordConfig.folderRecord = kwargs.get('folderRecord', recordConfig.folderRecord)
    recordConfig.fileNamePrint = kwargs.get('fileNamePrint', recordConfig.fileNamePrint)
    recordConfig.fileNameCallFunc = kwargs.get('fileNameCallFunc', recordConfig.fileNameCallFunc)
    recordConfig.fileNameLog = kwargs.get('fileNameLog', recordConfig.fileNameLog)

# decorator
def RecordCallFunc(func):
    def run(*args, **kwargs):
        localTime = time.localtime()
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        with open(recordConfig.fileCallFunc, 'a+', encoding='utf-8', newline='') as fw:
            fw.write(f'[Record][{func.__name__}][{localTime.tm_year}-{localTime.tm_mon}-{localTime.tm_mday} {localTime.tm_hour}:{localTime.tm_min}:{localTime.tm_sec}] has used {1000*(t1-t0)}ms\n')
        return result
    return run

# decorator
def RecordPrint(func):
    def run(*args, **kwargs):
        with open(recordConfig.filePrint, 'a+', encoding='utf-8', newline='') as fw:
            localTime = time.localtime()
            default_stdout = sys.stdout
            sys.stdout = fw
            print(recordConfig.header.center(recordConfig.lenStr, recordConfig.fillChar))
            print(f'[{func.__name__}][RunTime]: {localTime.tm_year}-{localTime.tm_mon}-{localTime.tm_mday} {localTime.tm_hour}:{localTime.tm_min}:{localTime.tm_sec}')
            t0 = time.time()
            result = func(*args, **kwargs)
            t1 = time.time()
            print(f'[{func.__name__}][UserTime]: {1000*(t1-t0)}ms')
            print(recordConfig.tailer.center(recordConfig.lenStr, recordConfig.fillChar))
            sys.stdout = default_stdout
        return result
    return run

def RecordLog(*args, **kwargs):
    lst = list(map(lambda i:str(i), args))
    fw = open(recordConfig.fileLog, 'a+', encoding='utf-8', newline='')
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    file = kwargs.get('file', fw)
    flush = kwargs.get('flush', False)
    print(*lst, sep=sep, end=end, file=file, flush=flush)
    if not fw.closed:
        fw.close()







if __name__ == '__main__':
    pass