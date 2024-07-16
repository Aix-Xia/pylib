import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import SymLogNorm, LogNorm
import math

GnRd1 = colors.LinearSegmentedColormap.from_list('rgy',
                                                [(0.0, (0.0, 1.0, 0.0)),
                                                 (0.5, (1.0, 1.0, 0.0)),
                                                 (1.0, (1.0, 0.0, 0.0))] )
GnRd2 = colors.LinearSegmentedColormap.from_list('rgy',
                                                [(0.0, (1.0, 0.0, 0.0)),
                                                 (0.5, (1.0, 1.0, 0.0)),
                                                 (1.0, (0.0, 1.0, 0.0))] )
def Heatmap(df, scale='linear', limit=None, vmaxRed=True, *, xline=None, yline=None):
    ysize, xsize = df.shape

    if ysize < 10:
        yticks = [i for i in range(ysize)]
    else:
        yticks = [i for i in range(0, ysize, math.ceil(ysize / 10))]

    if xsize < 10:
        xticks = [i for i in range(xsize)]
    else:
        xticks = [i for i in range(0, xsize, math.ceil(xsize / 10))]

    if limit == None:
        vmin = df.min().min()
        vmax = df.max().max()
    else:
        vmin = min(limit)
        vmax = max(limit)
    if scale == 'log':
        if vmax <= 0:
            vmax = 1
            vmin = 0.1
        elif vmin <= 0:
            vmin = 0.1 if (vmax > 0.1) else vmax / 100
        else:
            pass
        cticks = [vmin]
        for i in range(math.ceil(math.log10(vmin)), math.floor(math.log10(vmax))):
            cticks.append(10 ** i)
        cticks.append(vmax)
    elif scale == 'linear':
        cticks = [i for i in range(vmin, vmax + 1, math.ceil((vmax - vmin) / 10 + 1))]
    else:
        raise(ValueError(f'{scale} has not define'))

    fig, ax = plt.subplots()
    GnRd = GnRd1 if vmaxRed else GnRd2
    if scale == 'log':
        p = ax.imshow(df, norm=LogNorm(vmin=vmin, vmax=vmax), cmap=GnRd, aspect=1.4*xsize/ysize, interpolation='nearest')
    elif scale == 'linear':
        p = ax.imshow(df, cmap=GnRd, vmin=vmin, vmax=vmax, aspect=1.4*xsize/ysize, interpolation='nearest')
    else:
        raise(ValueError(f'{scale} has not define'))
    cbar = fig.colorbar(p, ax=ax)
    cbar.set_ticks(cticks)
    cbar.set_ticklabels([str(tick) for tick in cticks])

    plt.yticks([tick for tick in yticks], [str(tick) for tick in yticks])
    if type(xline) == list:
        for i in xline:
           plt.axhline(y=i + 0.5, linestyle="--", color="k", lw=0.5)

    plt.xticks([tick for tick in xticks], [str(tick) for tick in xticks], rotation=-60)
    if type(yline) == list:
        for i in yline:
            plt.axvline(x=i + 0.5, linestyle="--", color="k", lw=0.5)
    plt.show()

def CDF(axes, lst:list):
    length = len(lst)

    data = sorted(lst)
    cdf = [100 * i / (length-1) for i in range(length)]

    axes.plot(data, cdf)



if __name__ == '__main__':
    import pandas as pd

    df = pd.DataFrame([[0, 2, 3], [4, 5, 6]], index=list(range(2)), columns=list(range(3)))

    Heatmap(df, scale='log', vmaxRed=False, limit=(2, 7))