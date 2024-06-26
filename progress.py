from pylib import checker

class PROGRESS:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        self.barFill = '▓'
        self.spaceFill = ' '
        self.barLength = 50
    def __barFillSet(self, _value):
        if checker.Char(_value):
            self.__barFill = _value
    barFill = property(lambda self:self.__barFill, __barFillSet, lambda self:None, 'This is barFill!')
    def __spaceFillSet(self, _value):
        if checker.Char(_value):
            self.__spaceFill = _value
    spaceFill = property(lambda self:self.__spaceFill, __spaceFillSet, lambda self:None, 'This is spaceFill')
    def __barLengthSet(self, _value):
        if checker.NaturalNumber(_value, False):
            self.__barLength = _value
    barLength = property(lambda self:self.__barLength, __barLengthSet, lambda self:None, 'This is barLength!')
progresser = PROGRESS()

def SetProgressConfig(**kwargs):
    progresser.barFill = kwargs.get('barFill', progresser.barFill)
    progresser.spaceFill = kwargs.get('spaceFill', progresser.spaceFill)
    progresser.barLength = kwargs.get('barLength', progresser.barLength)

def PrintProgress(index:int, total:int, comment:str=''):
    if type(index) != int or type(total) != int or type(comment) != str:
        raise(TypeError('input parameter type error!'))
    if index <= 0 or total <= 0 or index > total:
        raise(ValueError('index or total value is error!'))
    _barCnt = progresser.barLength * index // total
    _spaceCnt = progresser.barLength - _barCnt
    _bar = '|' + progresser.barFill * _barCnt + progresser.spaceFill * _spaceCnt + '|'
    _progress = f'({index}/{total}, {100*index/total:3.1f}%)'
    _comment = f'正在处理：{comment}'
    print(f'\r{_bar}  {_progress}\t{_comment}', end='')
    if index == total:
        print()


if __name__ == '__main__':
    pass