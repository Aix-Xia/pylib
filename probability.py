from scipy.stats import binom



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


def Probability(sampleCount:int, occurProbability:float, occurCount:int):
    """
    :param sampleCount:样本量
    :param occurProbability:单个样本发生概率
    :param occurCount:样本发生个数
    :return:
    """
    return binom.pmf(occurCount, sampleCount, occurProbability)

def UBER(totalBitCount, ECC, RBER):
    probability = 0
    for ebc in range(ECC + 1, totalBitCount + 1):
        probability += Probability(totalBitCount, RBER, ebc)
    return probability / totalBitCount

if __name__ == '__main__':
    rberLst = [9.0e-09, 8.0e-09, 7.0e-09, 6.0e-09, 5.0e-09, 4.0e-09, 3.0e-09, 2.0e-09, 1.0e-09,
               9.0e-10, 8.0e-10, 7.0e-10, 6.0e-10, 5.0e-10, 4.0e-10, 3.0e-10, 2.0e-10, 1.0e-10,
               9.0e-11, 8.0e-11, 7.0e-11, 6.0e-11, 5.0e-11, 4.0e-11, 3.0e-11, 2.0e-11, 1.0e-11,
               9.0e-12, 8.0e-12, 7.0e-12, 6.0e-12, 5.0e-12, 4.0e-12, 3.0e-12, 2.0e-12, 1.0e-12,
               ]
    totalBitCount = 128 + 8
    ecc = 1
    for rber in rberLst:
        print(f'{rber} {UBER(totalBitCount, ecc, rber):.2e}')
