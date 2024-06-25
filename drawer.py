import matplotlib.pyplot as plt


def CDF(axes, lst:list):
    length = len(lst)

    data = sorted(lst)
    cdf = [100 * i / (length-1) for i in range(length)]

    axes.plot(data, cdf)



if __name__ == '__main__':
    import random
    lst = [random.random() for i in range(100000)]

    fig = plt.figure()
    axes = fig.add_subplot(1, 1, 1)
    CDF(axes, lst)



    plt.show()