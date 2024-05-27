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
    def __getNumerical(self)->bool:
        return self.__numerical
    def __setNumerical(self, value:bool):
        self.__numerical = bool(value)
    def __delNumerical(self):
        print('numerical has delete!')
    numerical = property(__getNumerical, __setNumerical, __delNumerical, 'This is numerical!')
    def __getLowerLetter(self)->bool:
        return self.__lowerLetter
    def __setLowerLetter(self, value:bool):
        self.__lowerLetter = bool(value)
    def __delLowerLetter(self):
        print('lowerLetter has delete!')
    lowerLetter = property(__getLowerLetter, __setLowerLetter, __delLowerLetter, 'This is lowerLetter!')
    def __getUpperLetter(self)->bool:
        return self.__upperLetter
    def __setUpperLetter(self, value:bool):
        self.__upperLetter = bool(value)
    def __delUpperLetter(self):
        print('upperLetter has delete!')
    upperLetter = property(__getUpperLetter, __setUpperLetter, __delUpperLetter, 'This is upperLetter!')
    def __getSpecialLetter(self)->bool:
        return self.__specialLetter
    def __setSpecialLetter(self, value:bool):
        self.__specialLetter = bool(value)
    def __delSpecialLetter(self):
        print('specialLetter has delete!')
    specialLetter = property(__getSpecialLetter, __setSpecialLetter, __delSpecialLetter, 'This is specialLetter!')
    def __getLength(self)->int:
        return self.__length
    def __setLength(self, value:int):
        if type(value) != int:
            raise(TypeError('length must set int type data!'))
        if value <= 0:
            raise(ValueError('length must set more than 0'))
        self.__length = value
    def __delLength(self):
        print('length has delete!')
    length = property(__getLength, __setLength, __delLength, 'This is length!')
    def __getOthers(self)->bool:
        return self.__others
    def __setOthers(self, value:bool):
        self.__others = bool(value)
    def __delOthers(self):
        print('others has delete!')
    others = property(__getOthers, __setOthers, __delOthers, 'This is others!')
    def __getRepeat(self)->bool:
        return self.__repeat
    def __setRepeat(self, value:bool):
        self.__repeat = bool(value)
    def __delRepeat(self):
        print('repeat has delete!')
    repeat = property(__getRepeat, __setRepeat, __delRepeat, 'This is repeat!')
    def __getDynamic(self)->bool:
        return self.__dynamic
    def __setDynamic(self, value:bool):
        self.__dynamic = bool(value)
    def __delDynamic(self):
        print('dynamic has delete!')
    dynamic = property(__getDynamic, __setDynamic, __delDynamic, 'This is dynamic!')
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
