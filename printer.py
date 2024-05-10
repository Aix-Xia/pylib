class Color:
    foreColorElement = (30, 31, 32, 33, 34, 35, 36, 37, '')
    backColorElement = (40, 41, 42, 43, 44, 45, 46, 47, ' ')
    def __init__(self, _name:str, _foreColor, _backColor):
        self.name = _name
        self.foreColor = _foreColor
        self.backColor = _backColor
    def _getName(self):
        return self._name
    def _setName(self, _value):
        self._name = str(_value)
    def _delName(self):
        print('name has delete!')
    name = property(_getName, _setName, _delName, 'This is name!')
    def _getForeColor(self):
        return self._foreColor
    def _setForeColor(self, _value:int):
        if _value not in Color.foreColorElement:
            raise(ValueError(f'{_value} is not define "foreColor" data!'))
        self._foreColor = _value
    def _delForeColor(self):
        print('foreColor has delete!')
    foreColor = property(_getForeColor, _setForeColor, _delForeColor, 'This is foreColor!')
    def _getBackColor(self):
        return self._backColor
    def _setBackColor(self, _value:int):
        if _value not in Color.backColorElement:
            raise (ValueError(f'{_value} is not define "backColor" data!'))
        self._backColor = _value
    def _delBackColor(self):
        print('backColor has delete!')
    backColor = property(_getBackColor, _setBackColor, _delBackColor, 'This is backColor!')
defaultColor = Color('Default', '', ' ')        # 默认
black = Color('Black', 30, 40)                  # 黑色
red = Color('Red', 31, 41)                      # 红色
green = Color('Green', 32, 42)                  # 绿色
yellow = Color('Yellow', 33, 43)                # 黄色
blue = Color('Blue', 34, 44)                    # 蓝色
purplishRed = Color('PurplishRed', 35, 45)      # 紫红
turquoiseBlue = Color('TurquoiseBlue', 36, 46)  # 青蓝
white = Color('White', 37, 47)                  # 白色

class Display:
    element = (0, 1, 4, 5, 7, 8)
    def __init__(self, _name, _display):
        self.name = _name
        self.display = _display
    def _getName(self):
        return self._name
    def _setName(self, _value):
        self._name = str(_value)
    def _delName(self):
        print('name has delete!')
    name = property(_getName, _setName, _delName, 'This is name!')
    def _getDisplay(self):
        return self._display
    def _setDisplay(self, _value):
        if _value not in Display.element:
            raise(ValueError(f'{_value} is not define "display" data!'))
        self._display = _value
    def _delDisplay(self):
        print('display has delete!')
    display = property(_getDisplay, _setDisplay, _delDisplay, 'This is display!')
defaultDisplay = Display('Default', 0)  # 默认
highLight = Display('HighLight', 1)     # 高亮
underLine = Display('UnderLine', 4)     # 下划线
flicker = Display('Flicker', 5)         # 闪烁
antiWhite = Display('Anti-White', 7)    # 反白
invisible = Display('Invisible', 8)     # 不可见

class PRINTER:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        self.display = defaultDisplay
        self.foreColor = defaultColor
        self.backColor = defaultColor
        self.TurnOn()
    def __del__(self):
        self.TurnOff()
    def _getDisplay(self):
        return self._display
    def _setDisplay(self, _value):
        if type(_value) == Display:
            self._display = _value.display
        elif _value in Display.element:
                self._display = _value
    def _delDisplay(self):
        print('display has delete!')
    display = property(_getDisplay, _setDisplay, _delDisplay, 'This is display!')
    def _getForeColor(self):
        return self._foreColor
    def _setForeColor(self, _value):
        if type(_value) == Color:
            self._foreColor = _value.foreColor
        elif _value in Color.foreColorElement:
            self._foreColor = _value
    def _delForeColor(self):
        print('foreColor has delete!')
    foreColor = property(_getForeColor, _setForeColor, _delForeColor, 'This is foreColor!')
    def _getBackColor(self):
        return self._backColor
    def _setBackColor(self, _value):
        if type(_value) == Color:
            self._backColor = _value.backColor
        elif _value in Color.backColorElement:
            self._backColor = _value
    def _delBackColor(self):
        print('backColor has delete!')
    backColor = property(_getBackColor, _setBackColor, _delBackColor, 'This is backColor!')
    @property
    def strStart(self):
        return f'\033[{self._display};{self._foreColor};{self._backColor}m'
    @property
    def strEnd(self):
        return f'\033[0m'
    @property
    def status(self):
        return self._status
    def Set(self, **kwargs):
        self.display = kwargs.get('display', self.display)
        self.foreColor = kwargs.get('foreColor', self.foreColor)
        self.backColor = kwargs.get('backColor', self.backColor)
        self.TurnOn()
    def TurnOn(self):
        print(self.strStart, end='')
        self._status = True
    def TurnOff(self):
        print(self.strEnd, end='')
        self._status = False
printer = PRINTER()


def Start(_display:Display, _foreColor:Color, _backColor:Color, _comment:str=''):
    if type(_display) != Display or type(_foreColor) != Color or type(_backColor) != Color:
        raise(TypeError('type error!'))
    print(f'\033[{_display.display};{_foreColor.foreColor};{_backColor.backColor}m', end=_comment)

def End():
    if printer.status:
        printer.TurnOn()
    else:
        printer.TurnOff()


def Print(*args, **kwargs):
    _display = kwargs.get('display', defaultDisplay)
    _foreColor = kwargs.get('foreColor', defaultColor)
    _backColor = kwargs.get('backColor', defaultColor)
    Start(_display, _foreColor, _backColor)
    _sep = kwargs.get('sep', None)
    _end = kwargs.get('end', None)
    _file = kwargs.get('file', None)
    _flush = kwargs.get('flush', None)
    print(*args, sep=_sep, end=_end, file=_file, flush=_flush)
    End()


_debugFlag = True
def DebugDisable():
    global _debugFlag
    _debugFlag = False
def DebugEnable():
    _debugFlag = True
def DebugPrint(*args, **kwargs):
    if not _debugFlag:
        return
    Start(defaultDisplay, blue, defaultColor, '[Debug] ')
    print(*args, **kwargs)
    End()
def WarnPrint(*args, **kwargs):
    Start(defaultDisplay, red, defaultColor, '[WARN] ')
    print(*args, **kwargs)
    End()


if __name__ == '__main__':
    DebugPrint(1, 2, 3)
