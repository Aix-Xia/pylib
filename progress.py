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
    def _barFillGet(self):
        return self._barFill
    def _barFillSet(self, _value):
        if check.Char(_value):
            self._barFill = _value
    def _barFillDel(self):
        print('barFill has delete!')
    barFill = property(_barFillGet, _barFillSet, _barFillDel, 'This is barFill!')
    def _spaceFillGet(self):
        return self._spaceFill
    def _spaceFillSet(self, _value):
        if check.Char(_value):
            self._spaceFill = _value
    def _spaceFillDel(self):
        print('spaceFill has delete!')
    spaceFill = property(_spaceFillGet, _spaceFillSet, _spaceFillDel, 'This is spaceFill')
    def _barLengthGet(self):
        return self._barLength
    def _barLengthSet(self, _value):
        if check.NaturalNumber(_value, False):
            self._barLength = _value
    def _barLengthDel(self):
        print('barLength has delete!')
    barLength = property(_barLengthGet, _barLengthSet, _barLengthDel, 'This is barLength!')
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