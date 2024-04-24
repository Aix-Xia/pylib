_barFill = '▓'
_spaceFill = ' '
_barLength = 50

def SetProgressConfig(**kwargs):
    global _barFill, _spaceFill, _barLength
    _barFill = kwargs.get('barFill', _barFill)
    _spaceFill = kwargs.get('spaceFill', _spaceFill)
    _barLength = kwargs.get('barLength', _barLength)

def PrintProgress(index:int, total:int, comment:str=''):
    if type(index) != int or type(total) != int or type(comment) != str:
        raise(TypeError('input parameter type error!'))
    if index <= 0 or total <= 0 or index > total:
        raise(ValueError('index or total value is error!'))
    _barCnt = _barLength * index // total
    _spaceCnt = _barLength - _barCnt
    _bar = '|' + _barFill * _barCnt + _spaceFill * _spaceCnt + '|'
    _progress = f'({index}/{total}, {100*index/total:3.1f}%)'
    _comment = f'正在处理：{comment}'
    print(f'\r{_bar}{_progress}\t{_comment}', end='')
    if index == total:
        print()