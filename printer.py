class Color:
    foreColorElement = (30, 31, 32, 33, 34, 35, 36, 37, '')
    backColorElement = (40, 41, 42, 43, 44, 45, 46, 47, ' ')
    def __init__(self, _name:str, _foreColor, _backColor):
        self.name = _name
        self.foreColor = _foreColor
        self.backColor = _backColor
    def _setName(self, _value):
        self.__name = str(_value)
    name = property(lambda self:self.__name, _setName, lambda self:None, 'This is name!')
    def _setForeColor(self, _value:int):
        if _value not in Color.foreColorElement:
            raise(ValueError(f'{_value} is not define "foreColor" data!'))
        self.__foreColor = _value
    foreColor = property(lambda self:self.__foreColor, _setForeColor, lambda self:None, 'This is foreColor!')
    def _setBackColor(self, _value:int):
        if _value not in Color.backColorElement:
            raise (ValueError(f'{_value} is not define "backColor" data!'))
        self.__backColor = _value
    backColor = property(lambda self:self.__backColor, _setBackColor, lambda self:None, 'This is backColor!')
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
    element = (0, 1, 3, 4, 5, 7, 8)
    def __init__(self, _name, _display):
        self.name = _name
        self.display = _display
    def __setName(self, _value):
        self.__name = str(_value)
    name = property(lambda self:self.__name, __setName, lambda self:None, 'This is name!')
    def __setDisplay(self, _value):
        if _value not in Display.element:
            raise(ValueError(f'{_value} is not define "display" data!'))
        self.__display = _value
    display = property(lambda self:self.__display, __setDisplay, lambda self:None, 'This is display!')
defaultDisplay = Display('Default', 0)  # 默认
highLight = Display('HighLight', 1)     # 高亮
italic = Display('Italic', 3)           # 斜体
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
    def __displaySet(self, _value):
        if type(_value) == Display:
            self.__display = _value.display
        elif _value in Display.element:
                self.__display = _value
    display = property(lambda self:self.__display, __displaySet, lambda self:None, 'This is display!')
    def __foreColorSet(self, _value):
        if type(_value) == Color:
            self.__foreColor = _value.foreColor
        elif _value in Color.foreColorElement:
            self.__foreColor = _value
    foreColor = property(lambda self:self.__foreColor, __foreColorSet, lambda self:None, 'This is foreColor!')
    def __setBackColor(self, _value):
        if type(_value) == Color:
            self.__backColor = _value.backColor
        elif _value in Color.backColorElement:
            self.__backColor = _value
    backColor = property(lambda self:self.__backColor, __setBackColor, lambda self:None, 'This is backColor!')
    @property
    def strStart(self):
        return f'\033[{self.__display};{self.__foreColor};{self.__backColor}m'
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
    Start(defaultDisplay, green, defaultColor, '[Debug] ')
    print(*args, **kwargs)
    End()
def WarnPrint(*args, **kwargs):
    Start(defaultDisplay, red, defaultColor, '[WARN] ')
    print(*args, **kwargs)
    End()


if __name__ == '__main__':
    DebugPrint("args")
