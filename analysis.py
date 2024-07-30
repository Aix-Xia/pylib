""" data processing"""
import math
import sympy

def dmin(lst:list or int or float, base=None)->int or float:
    """get min data in lst"""
    for data in lst:
        if type(data) == list:
            base = dmin(data, base)
        elif type(data) == int or type(data) == float:
            if base == None or data < base:
                base = data
    return base

def dmax(lst:list or int or float, base=None)->int or float:
    """get max data in lst"""
    for data in lst:
        if type(data) == list:
            base = dmax(data, base)
        elif type(data) == int or type(data) == float:
            if base == None or data > base:
                base = data
    return base

def is_power_number(number:int, base:int)->bool:
    """
    判断data是否为base的整数次幂
    :param data:
    :param base:
    :return: bool
    """
    if type(number) != int:
        raise TypeError('"data" must "int" type!!!  %s is not "int" type!' % str(number))
    if type(base) != int:
        raise TypeError('"base" must "int" type!!!  %s is not "int" type!' % str(base))
    if number <= 0:
        raise ValueError('"data" must bigger than 0')
    if base <= 1:
        raise ValueError('"base" must bigger than 1')
    complement = 0
    while True:
        if number < base or (complement != 0):
            break
        complement = number % base
        number = number // base
    if number == 1 and complement == 0:
        result = True
    else:
        result = False
    return result

def is_power2_number(number:int)->bool:
    """
        判断data是否为 2 的整数次幂
        :param data:
        :return: bool
    """
    if type(number) != int:
        raise TypeError('"data" must "int" type!!!  %s is not "int" type!' % str(number))
    if number <= 0:
        raise ValueError('"data" must bigger than 0')

    if number & (number - 1):
        return False
    else:
        return True

def is_prime_number(number:int)->bool:
    """
    判断number是否为质数
    :param number:
    :return: bool
    """
    if type(number) != int:
        raise TypeError('"n" must "int" type!!!  %s is not "int" type!' % number)
    if number < 2:
        raise ValueError('"n" must bigger than 1')
    for i in range(2, number):
        if number % i == 0:
            return False
    return True

def eviation(func): # Decorator
    def run(*args, **kwargs):
        def list_normalize(lst, *args):
            for data in args:
                if type(data) == list or type(data) == tuple or type(data) == set:
                    list_normalize(lst, *data)
                elif type(data) == int or type(data) == float:
                    lst.append(data)
                else:
                    raise (TypeError(f'{data} is not define type'))
        lst = []
        list_normalize(lst, *args)
        result = func(lst, **kwargs)
        return result
    return run

def average(dlst):
    """
    计算dlst列表中所有数据的平均值
    :param dlst: 数据列表 list(int / float)
    :return: 平均值
    """
    return sum(dlst) / len(dlst)

@eviation
def variance(dlst, **kwargs):
    """
    计算dlst列表中所有数据的方差
    :param dlst: 数据列表 list(int / float)
    :param standard: 标准偏差
    :return: 方差
    """
    standard = kwargs.get('standard', True)
    n = len(dlst)
    avg = average(dlst)
    varis_n = 0
    for i in range(n):
        varis_n += (dlst[i] - avg) ** 2
    varis = varis_n / (n - int(standard))
    return varis

@eviation
def stdev(dlst, **kwargs):
    """
    计算dlst列表中所有数据的标准差
    :param 数据列表 list(int / float)
    :param standard: 标准偏差
    :return: 标准差
    """
    standard = kwargs.get('standard', True)
    varis = variance(dlst, standard)
    std = math.sqrt(varis)
    return std

def fit_line(xlst, ylst):
    """
    :param xlst: x坐标 列表
    :param ylst: y坐标 列表
    :return: 计算获得: y = kx + b
    """
    n = len(xlst) if len(xlst)==len(ylst) else 0
    if n==0:
        raise(ValueError('len(xlst) must eq len(ylst)'))

    x_avg = sum(xlst)/n
    y_avg = sum(ylst)/n

    xy_sum = 0
    xx_sum = 0
    for i in range(n):
        xy_sum += xlst[i]*ylst[i]
        xx_sum += xlst[i]*xlst[i]
    k = (xy_sum - n * x_avg * y_avg) / (xx_sum - n * x_avg * x_avg)
    b = y_avg - k * x_avg

    rxlst = [min(xlst), max(xlst)]
    rylst = [k * x + b for x in rxlst]
    return rxlst, rylst

def SolutionEquations(coefficientMatrix, resultList, elementList=None):
    parameterTypeSet = (list, tuple)
    dataTypeSet = (int, float)

    if type(resultList) not in parameterTypeSet:
        raise(TypeError('resultList Type Error'))
    length = len(resultList)
    for data in range(length):
        if type(data) not in dataTypeSet:
            raise(TypeError('resultList Type Error'))

    if type(coefficientMatrix) not in parameterTypeSet:
        raise (TypeError('coefficientMatrix Type Error'))
    if len(coefficientMatrix) != length:
        raise (ValueError('coefficientMatrix Value Error'))
    for item in coefficientMatrix:
        if type(item) not in parameterTypeSet:
            raise (TypeError('coefficientMatrix Type Error'))
        if len(item) != length:
            raise (ValueError('coefficientMatrix Value Error'))
        for num in item:
            if type(num) not in dataTypeSet:
                raise (TypeError('coefficientMatrix Type Error'))

    if elementList != None:
        if type(elementList) not in parameterTypeSet:
            raise (TypeError('elementList Type Error'))
        if len(elementList) != length:
            raise (ValueError('elementList value Error'))
        for i in elementList:
            if type(i) != str:
                raise (TypeError('elementList Type Error'))

    if elementList == None:
        pList = [sympy.symbols('X'+str(i)) for i in range(length)]
    else:
        pList = [sympy.symbols(i) for i in elementList]
    eqString = '['
    for i in range(length):
        iString = f'sympy.Eq(coefficientMatrix[{i}][0] * pList[0]'
        for j in range(1, length):
            iString += f' + coefficientMatrix[{i}][{j}] * pList[{j}]'
        iString += f', resultList[{i}]),'
        eqString += iString
    eqString = eqString[:-1]
    eqString += ']'
    eqSet = eval(eqString)
    result = sympy.solve(eqSet, pList)
    return result

if __name__ == '__main__':
    a = [1,2,3,4,5,6,6, [1,2, 3]]
    print(variance(a, standard=True))
