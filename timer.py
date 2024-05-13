import time

def GetDurationStr(_time:float)->str:
    """
    将通过 两个time.time()获取的时间转换成字符串
    """
    try:
        _time = float(_time)
        if _time < 0:
            raise(f'{_time} do not match request!')
    except Exception:
        raise (f'{_time} do not match request!')
    if _time < 0.000001:
        return f'{1000000000 * _time:.2f} ns'
    elif _time < 0.001:
        return f'{1000000 * _time:.2f} us'
    elif _time < 1:
        return f'{1000 * _time:.2f} ms'
    elif _time < 60:
        return f'{_time:.2f} s'
    elif _time < 3600:
        return f'{_time / 60:.2f} min'
    else:
        return f'{_time / 3600:.2f} h'


class TIMER:
    _statusSet = ('Init', 'Pause', 'Run', 'Stop')
    def __init__(self):
        self.Init()
    def __dir__(self):
        return ('Init', 'Start', 'Pause', 'Restart', 'Stop', 'PrintTimeAccumulate', 'PrintLastUse')
    # def __del__(self):
    #     self.Stop()
    @property
    def timeCurrent(self):
        return time.time()
    @property
    def timeAccumulate(self):
        return self._timeAccumulate
    @property
    def timeLast(self):
        if self.status == 'Run':
            return self.timeCurrent - self._timeStart
        else:
            return self._timeStop - self._timeStart
    def _getStatus(self):
        return self._status
    def _setStatus(self, _value):
        if _value in TIMER._statusSet:
            self._status = _value
    def _delStatus(self):
        print('status has delete!')
    status = property(_getStatus, _setStatus, _delStatus, 'This is status!')
    def Init(self):
        self._timeAccumulate = 0
        self._timeStart = 0
        self._timeStop = 0
        self._status = 'Init'
    def Start(self):
        if self.status == 'Init':
            self._timeStart = self.timeCurrent
            self.status = 'Run'
        elif self.status == 'Pause':
            self.Restart()
        elif self.status == 'Run':
            print('Current status is "Run", can not using "Start" function. Has not do anything!')
        elif self.status == 'Stop':
            self.Init()
            self.Start()
        else:
            raise(f'"{self._status}" has not define, pls check!')
    def Pause(self):
        if self.status == 'Init':
            print('Current status is "Init", can not using "Pause" function. Has not do anything!')
        elif self.status == 'Pause':
            print('Current status is "Pause", can not using "Pause" function. Has not do anything!')
        elif self.status == 'Run':
            self._timeStop = self.timeCurrent
            self._timeAccumulate += (self._timeStop - self._timeStart)
            self.status = 'Pause'
        elif self.status == 'Stop':
            print('Current status is "Stop", can not using "Pause" function. Has not do anything!')
        else:
            raise (f'"{self._status}" has not define, pls check!')
    def Restart(self):
        if self.status == 'Init':
            print('Current status is "Init", can not using "Restart" function. Has not do anything!')
        elif self.status == 'Pause':
            self._timeStart = self.timeCurrent
            self.status = 'Run'
        elif self.status == 'Run':
            print('Current status is "Run", can not using "Restart" function. Has not do anything!')
        elif self.status == 'Stop':
            self._timeStart = self.timeCurrent
            self.status = 'Run'
        else:
            raise (f'"{self._status}" has not define, pls check!')
    def Stop(self):
        if self.status == 'Init':
            print('Current status is "Init", can not using "Stop" function. Has not do anything!')
        elif self.status == 'Pause':
            self.status = 'Stop'
        elif self.status == 'Run':
            self.Pause()
            self.Stop()
        elif self.status == 'Stop':
            print('Current status is "Stop", can not using "Stop" function. Has not do anything!')
        else:
            raise (f'"{self._status}" has not define, pls check!')
    def PrintTimeAccumulate(self, symbol='Debug'):
        print(f'[{symbol}] Accumulate time: {GetDurationStr(self.timeAccumulate)}')
    def PrintTimeLast(self, symbol='Debug'):
        print(f'[{symbol}] Last time: {GetDurationStr(self.timeLast)}')


_funcRunTimer = {}
def DecoratorFuncRunTime(func):
    if func.__name__ not in _funcRunTimer:
        _funcRunTimer[func.__name__] = TIMER()
    def run(*args, **kwargs):
        _funcRunTimer[func.__name__].Start()
        result = func(*args, **kwargs)
        _funcRunTimer[func.__name__].Pause()
        _funcRunTimer[func.__name__].PrintTimeLast(func.__name__)
        return result
    return run
def PrintFuncTimeAccumulate(funcName:str=None):
    if funcName == None:
        for _key, _timer in _funcRunTimer.items():
            _timer.PrintTimeAccumulate(_key)
    elif funcName not in _funcRunTimer:
        print(f'[{funcName}] has not be called!')
    else:
        _funcRunTimer[funcName].PrintTimeAccumulate(funcName)

if __name__ == '__main__':
    print(GetDurationStr(0.0000002))