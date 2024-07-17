import random


class RandomString:
    __lstOther = []
    __lstNumerical = [i for i in '0123456789']
    __lstLowerLetter = [i for i in 'abcdefghijklmnopqrstuvwxyz']
    __lstUpperLetter = [i for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    __lstSpecialLetter = [i for i in '!#$%&()*+,-./:;<=>?@[]^_`{|}~']
    def __init__(self):
        self.length = 6
        self.numerical = True
        self.lowerLetter = True
        self.upperLetter = True
        self.specialLetter = False
        self.others = False
        self.repeat = True
        self.dynamic = False
        self.__string = ''
        self.Refresh()
    def __str__(self):
        if self.dynamic:
            self.Refresh()
        return self.__string
    def __call__(self):
        if self.dynamic:
            self.Refresh()
        return self.__string
    def __setNumerical(self, value:bool):
        self.__numerical = bool(value)
    numerical = property(lambda self:self.__numerical, __setNumerical, lambda self:None, 'This is numerical!')
    def __setLowerLetter(self, value:bool):
        self.__lowerLetter = bool(value)
    lowerLetter = property(lambda self:self.__lowerLetter, __setLowerLetter, lambda self:None, 'This is lowerLetter!')
    def __setUpperLetter(self, value:bool):
        self.__upperLetter = bool(value)
    upperLetter = property(lambda self:self.__upperLetter, __setUpperLetter, lambda self:None, 'This is upperLetter!')
    def __setSpecialLetter(self, value:bool):
        self.__specialLetter = bool(value)
    specialLetter = property(lambda self:self.__specialLetter, __setSpecialLetter, lambda self:None, 'This is specialLetter!')
    def __setLength(self, value:int):
        if type(value) != int:
            raise(TypeError('length must set int type data!'))
        if value <= 0:
            raise(ValueError('length must set more than 0'))
        self.__length = value
    length = property(lambda self:self.__length, __setLength, lambda self:None, 'This is length!')
    def __setOthers(self, value:bool):
        self.__others = bool(value)
    others = property(lambda self:self.__others, __setOthers, lambda self:None, 'This is others!')
    def __setRepeat(self, value:bool):
        self.__repeat = bool(value)
    repeat = property(lambda self:self.__repeat, __setRepeat, lambda self:None, 'This is repeat!')
    def __setDynamic(self, value:bool):
        self.__dynamic = bool(value)
    dynamic = property(lambda self:self.__repeat, __setDynamic, lambda self:None, 'This is dynamic!')
    def Config(self, length:int, **kwargs):
        self.length = length
        self.numerical = kwargs.get('numerical', self.numerical)
        self.lowerLetter = kwargs.get('lowerLetter', self.lowerLetter)
        self.upperLetter = kwargs.get('upperLetter', self.upperLetter)
        self.specialLetter = kwargs.get('specialLetter', self.specialLetter)
        self.others = kwargs.get('others', self.others)
        self.repeat = kwargs.get('repeat', self.repeat)
        self.dynamic = kwargs.get('dynamic', self.dynamic)
        self.Refresh()
    def Refresh(self):
        lst = []
        if self.numerical:
            lst.extend(RandomString.__lstNumerical)
        if self.lowerLetter:
            lst.extend(RandomString.__lstLowerLetter)
        if self.upperLetter:
            lst.extend(RandomString.__lstUpperLetter)
        if self.specialLetter:
            lst.extend(RandomString.__lstSpecialLetter)
        if self.others:
            lst.extend(RandomString.__lstOther)
        lst = list(set(lst))
        result = ''
        for i in range(self.length):
            length = len(lst)
            if length == 0:
                raise (ValueError('lst has not sample'))
            index = random.randint(0, length - 1)
            result += lst[index]
            if not self.repeat:
                lst = lst[:index] + lst[index + 1:]
        self.__string = result
    @property
    def value(self):
        return self.__string
    @classmethod
    def AppendOtherList(cls, *args):
        for value in args:
            if type(value) != str:
                raise(TypeError(f'{value} is not "str" type data'))
            for i in value:
                if i not in cls.__lstOther:
                    cls.__lstOther.append(i)
    @classmethod
    def DeleteOtherList(cls, *args):
        for value in args:
            if type(value) != str:
                raise (TypeError(f'{value} is not "str" type data'))
            for i in value:
                if i in cls.__lstOther:
                    cls.__lstOther.remove(i)



if __name__ == '__main__':
    psw = RandomString()
    # RandomString.AppendOtherList('1234567', 'abcd')
    psw.Config(6, numerical=True, lowerLetter=False, upperLetter=False, specialLetter=False, others=False, repeat=True, dynamic=True)

    for i in range(20):
        print(psw, end='\t')
        a = psw()
        print(a)
