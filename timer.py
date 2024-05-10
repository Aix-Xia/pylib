import time




class TIMER:
    _statusSet = ('Init', 'Pause', 'Run', 'Stop')
    def __init__(self):
        self.Init()
    def __dir__(self):
        return ('Start', 'Restart', 'Pause', 'Init')
    @property
    def timeCurrent(self):
        return time.time()
    @property
    def timeAccumulate(self):
        return self._timeAccumulate
    @property
    def timeUse(self):
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
        self._status = TIMER._statusSet[0]
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
    def PrintTimeAccumulate(self, unit='s'):
        unit = unit.lower()
        coefficient = 1
        if unit == 's':
            coefficient *= 1
        elif unit == 'ms':
            coefficient *= 1000
        elif unit == 'us':
            coefficient *= 1000000
        elif unit == 'ns':
            coefficient *= 1000000000
        else:
            raise(ValueError(f'{unit} has not define, pls check!'))
        print(f'total has using {coefficient * self.timeAccumulate} {unit}')
    def PrintTimeUse(self, unit='s'):
        unit = unit.lower()
        coefficient = 1
        if unit == 's':
            coefficient *= 1
        elif unit == 'ms':
            coefficient *= 1000
        elif unit == 'us':
            coefficient *= 1000000
        elif unit == 'ns':
            coefficient *= 1000000000
        else:
            raise(ValueError(f'{unit} has not define, pls check!'))
        print(f'total has using {coefficient * self.timeUse} {unit}')