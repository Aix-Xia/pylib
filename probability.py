import math


def C(n:int, m:int)->int:
    if type(n) != int or type(m) != int:
        raise(TypeError('m,n must int type'))
    if m < 0 or n <= 0 or m > n:
        raise(ValueError('m, n do not match rule'))
    result = 1
    for i in range(m):
        result = result * (n - i) // (i + 1)
    return result

def A(n:int, m:int)->int:
    if type(n) != int or type(m) != int:
        raise(TypeError('m,n must int type'))
    if m < 0 or n <= 0 or m > n:
        raise(ValueError('m, n do not match rule'))
    result = 1
    for i in range(m):
        result = result * (n - i)
    return result


def GetRate(totalUnitCnt:int, lessUnitCnt:int, unitRate:float):
    result = 0
    for unitCnt in range(lessUnitCnt, totalUnitCnt + 1):
        rate = 1    # C(totalUnitCnt, unitCnt)
        for i in range(unitCnt):
            rate *= unitRate
            rate *= (totalUnitCnt - i)
            rate /= (i + 1)
        for i in range(unitCnt, totalUnitCnt):
            rate *= (1 - unitRate)
        result += rate
    return result

# def GetRate1(totalUnitCnt, lessUnitCnt, unitRate):
#     return sum([math.factorial(totalUnitCnt)/(math.factorial(i) * math.factorial(totalUnitCnt-i)) * unitRate**i * (1-unitRate)**(totalUnitCnt-i) for i in range(lessUnitCnt, totalUnitCnt+1)])





if __name__ == '__main__':
    N = 10
    m = 7
    p = 0.6
    print(GetRate(N, m, p))