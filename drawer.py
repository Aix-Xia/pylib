import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import SymLogNorm, LogNorm
from scipy.stats import linregress
import numpy as np
import pandas as pd
dpi = 600
GnRd1 = colors.LinearSegmentedColormap.from_list('rgy', [(0.0, (0.0, 1.0, 0.0)), (0.5, (1.0, 1.0, 0.0)), (1.0, (1.0, 0.0, 0.0))])
GnRd2 = colors.LinearSegmentedColormap.from_list('rgy', [(0.0, (1.0, 0.0, 0.0)), (0.5, (1.0, 1.0, 0.0)), (1.0, (0.0, 1.0, 0.0))])
def Heatmap(df, *, vmin:int or float=None, vmax:int or float=None, vmaxRed:bool=True, scale:str='linear', xline:list=None, yline:list=None, aspect:int or float=1, xticks:list=None, yticks:list=None, cticks:list=None, title:str=None, save:str=None, show:bool=True):
    ysize, xsize = df.shape
    GnRd = GnRd1 if vmaxRed else GnRd2

    vmin = (df.min() if (type(df) == np.ndarray) else df.min().min()) if (vmin == None) else vmin
    vmax = (df.max() if (type(df) == np.ndarray) else df.max().max()) if (vmax == None) else vmax

    if scale == 'log':
        if vmax <= 0:
            raise(ValueError('vmax can not less than 0 then scale is log'))
        elif vmin <= 0:
            vmin = min(vmax/100, 0.9)
        p = plt.imshow(df, norm=LogNorm(vmin=vmin, vmax=vmax), cmap=GnRd, aspect=aspect*xsize/ysize, interpolation='nearest')
    elif scale == 'linear':
        p = plt.imshow(df, cmap=GnRd, vmin=vmin, vmax=vmax, aspect=aspect*xsize/ysize, interpolation='nearest')
    else:
        raise(ValueError(f'{scale} has not define'))

    if yticks != None:
        plt.yticks([tick for tick in yticks], [str(tick) for tick in yticks])
    if xticks != None:
        plt.xticks([tick for tick in xticks], [str(tick) for tick in xticks], rotation=-60)
    if type(xline) in [list, tuple]:
        for i in xline:
            plt.axhline(y=i + 0.5, linestyle="--", color="k", lw=0.3)
    if type(yline) in [list, tuple]:
        for i in yline:
            plt.axvline(x=i + 0.5, linestyle="--", color="k", lw=0.3)

    cbar = plt.colorbar(p)
    if type(cticks) in [list, tuple]:
        cbar.set_ticks(cticks)
        cbar.set_ticklabels([f'{tick}' for tick in cticks])
    if title:
        plt.title(title)
    if show:
        plt.show()
    if save:
        plt.savefig(save, dpi=dpi, bbox_inches='tight')
    if show or save:
        plt.clf()
        plt.close()

def Histograms(series, *, vmin=None, vmax=None, step=None, title=None, xscale='linear', yscale='linear', save:str=None, show:bool=True):
    vmin = min(series) if vmin == None else vmin
    vmax = max(series) if vmax == None else vmax
    step = (vmax - vmin) / 20 if step == None else step
    bins = np.arange(vmin, vmax + step, step)
    plt.hist(series, bins)
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.xticks(bins, [f'{i:.02f}' for i in bins], rotation=-60)
    plt.grid()
    if title:
        plt.title(title)
    if show:
        plt.show()
    if save:
        plt.savefig(save, dpi=dpi, bbox_inches='tight')
    if show or save:
        plt.clf()

def Scatter(x, y, polyFit:int=1, *, xticks:list=None, yticks:list=None, title:str=None, save:str=None, show:bool=True):
    plt.scatter(x, y, s=5)

    count = 100
    expandRate = 0.05
    z = np.polyfit(x, y, polyFit)
    p = np.poly1d(z)
    vmin = np.min(x)
    vmax = np.max(x)
    expand = expandRate * (vmax - vmin)
    vmin = vmin - expand
    vmax = vmax + expand
    step = (vmax - vmin) / count
    xn = [vmin] + [vmin + i * step for i in range(count)]
    plt.plot(xn, p(xn), color='red')

    formula = f'f(X) = {z[0]:.2f}*X{polyFit}'
    for i in range(polyFit):
        formula += f' + {z[i+1]:.2f}*X{polyFit-i-1}'
    formula = formula[:-3]
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    formula = f'{formula}\nR2 = {r_value ** 2:.3f}'
    plt.annotate(formula, xy=(vmin, p(vmin)))

    if xticks:
        plt.xticks(xticks, [str(xtick) for xtick in xticks])
    if yticks:
        plt.yticks(yticks, [str(ytick) for ytick in yticks])
    if title:
        plt.title(title)
    if show:
        plt.show()
    if save:
        plt.savefig(save, dpi=dpi, bbox_inches='tight')
    if show or save:
        plt.clf()

def CDF(iterable, legend:str, *, title:str=None, xticks:list=None, save:str=None, show:bool=True):
    length = len(iterable)
    data = np.sort(iterable)
    cdf = [100 * i / (length - 1) for i in range(length)]
    plt.plot(data, cdf, label=legend)

    if xticks:
        plt.xticks(xticks, [str(i) for i in xticks])
    plt.yticks([10 * i for i in range(11)], [str(10 * i) + '%' for i in range(11)])
    plt.ylabel('percentage')

    if title:
        plt.title(title)
    if show or save:
        plt.grid()
        plt.legend()
    if show:
        plt.show()
    if save:
        plt.savefig(save, dpi=dpi, bbox_inches='tight')
    if show or save:
        plt.clf()

def Boxplot(df, *, yticks:list=None, title:str=None, xlabel:str=None, ylabel:str=None, save:str=None, show:bool=True):
    plt.boxplot(df)
    columns = df.columns.to_list()
    plt.xticks([i + 1 for i in range(len(columns))], columns)
    if xlabel:
        plt.xlabel(str(xlabel))
    if yticks:
        plt.yticks(yticks, [str(tick) for tick in yticks])
    if ylabel:
        plt.ylabel(str(ylabel))
    if title:
        plt.title(str(title))
    plt.grid()
    if show:
        plt.show()
    if save:
        plt.savefig(save, dpi=dpi, bbox_inches='tight')
    if show or save:
        plt.clf()

if __name__ == '__main__':
    pass