import matplotlib.pyplot as plt
import numpy as np
from collections import Iterable
from scipy.stats import linregress


# plt figure Setting
dpi = 600
axesKey = ('title', 'grid', 'legend',
           'xticks', 'xlabel', 'xscale', 'axhline', 'xlim',
           'yticks', 'ylabel', 'yscale', 'axvline', 'ylim')
axisKey = ('right', 'left', 'top', 'bottom')
figKey = ('suptitle', 'show', 'savefig', 'clf')
def SetAxes(ax=None, **kwargs):
    """
    :param ax:
    :param kwargs:  title, grid, legend
                    xticks, xlabel, xscale, axhline, xlim
                    yticks, ylabel, yscale, axvline, ylim
    """
    ax = plt.gca() if ax==None else ax

    title = kwargs.get('title', None)
    if title:
        ax.set_title(str(title))

    xlabel = kwargs.get('xlabel', None)
    if xlabel:
        ax.set_xlabel(xlabel)

    ylabel = kwargs.get('ylabel', None)
    if ylabel:
        ax.set_ylabel(ylabel)

    xticks = kwargs.get('xticks', None)
    if xticks:
        if type(xticks) not in [tuple, list]:
            raise(TypeError('xticks must tuple or list type'))
        xtickList = []
        xlabelList = []
        allNum = True
        for xtick in xticks:
            if type(xtick) not in (float, int):
                xtickList = []
                xlabelList = []
                allNum = False
                break
            else:
                xtickList.append(xtick)
                xlabelList.append(str(xtick))
        if allNum:
            ax.set_xticks(xtickList, xlabelList)
        else:
            if len(xticks) < 2:
                raise(ValueError('xticks has error'))
            if len(xticks[0]) != len(xticks[1]):
                raise(ValueError('xticks length has error'))
            for i in range(len(xticks[0])):
                if type(xticks[0][i]) not in (int, float):
                    raise(ValueError('xtick value has error'))
                xtickList.append(xticks[0][i])
                xlabelList.append(str(xticks[1][i]))
            ax.set_xticks(xtickList, xlabelList)

    yticks = kwargs.get('yticks', None)
    if yticks:
        if type(yticks) not in [tuple, list]:
            raise(TypeError('yticks must tuple or list type'))
        ytickList = []
        ylabelList = []
        allNum = True
        for ytick in yticks:
            if type(ytick) not in (float, int):
                ytickList = []
                ylabelList = []
                allNum = False
                break
            else:
                ytickList.append(ytick)
                ylabelList.append(str(ytick))
        if allNum:
            ax.set_yticks(ytickList, ylabelList)
        else:
            if len(yticks) < 2:
                raise(ValueError('yticks has error'))
            if len(yticks[0]) != len(yticks[1]):
                raise(ValueError('yticks length has error'))
            for i in range(len(yticks[0])):
                if type(yticks[0][i]) not in (int, float):
                    raise(ValueError('ytick value has error'))
                ytickList.append(yticks[0][i])
                ylabelList.append(str(yticks[1][i]))
            ax.set_yticks(ytickList, ylabelList)

    axvline = kwargs.get('axvline', None)
    if axvline != None:
        if type(axvline) in (int, float):
            ax.axvline(axvline, linestyle="--", color="k", lw=0.5)
        elif isinstance(axvline, Iterable):
            for x in axvline:
                ax.axvline(x, linestyle="--", color="k", lw=0.5)
        else:
            raise(TypeError('axvline type error'))

    axhline = kwargs.get('axhline', None)
    if axhline != None:
        if type(axhline) in (int, float):
            ax.axhline(axhline, linestyle="--", color="k", lw=0.5)
        elif isinstance(axhline, Iterable):
            for y in axhline:
                ax.axhline(y, linestyle="--", color="k", lw=0.5)
        else:
            raise (TypeError('axvline type error'))

    xlim = kwargs.get('xlim', None)
    if xlim:
        ax.set_xlim(xlim)

    ylim = kwargs.get('ylim', None)
    if ylim:
        ax.set_ylim(ylim)

    xscale = kwargs.get('xscale', None)
    if xscale:
        ax.set_xscale(xscale)

    yscale = kwargs.get('yscale', None)
    if yscale:
        ax.set_yscale(yscale)

    grid = kwargs.get('grid', False)
    if grid:
        ax.grid()

    lagend = kwargs.get('legend', False)
    if lagend:
        ax.legend()
def SetAxis(ax=None, **kwargs):
    """
    :param ax:
    :param kwargs: right, left, top, bottom
    """
    ax = plt.gca() if ax==None else ax

    right = kwargs.get('right', None)
    if right:
        ax.spines['right'].set_color(right[0])
        ax.spines['right'].set_position(('data', right[1]))

    left = kwargs.get('left', None)
    if left:
        ax.spines['left'].set_color(left[0])
        ax.spines['left'].set_position(('data', left[1]))

    top = kwargs.get('top', None)
    if top:
        ax.spines['top'].set_color(top[0])
        ax.spines['top'].set_position(('data', top[1]))

    bottom = kwargs.get('bottom', None)
    if bottom:
        ax.spines['bottom'].set_color(bottom[0])
        ax.spines['bottom'].set_position(('data', bottom[1]))
def SetFig(**kwargs):
    """
    :param kwargs:  suptitle, show, savefig, clf
    """
    suptitle = kwargs.get('suptitle', None)
    if suptitle:
        plt.suptitle(suptitle)

    show = kwargs.get('show', False)
    if show:
        plt.show()

    savefig = kwargs.get('savefig', None)
    if savefig:
        plt.savefig(savefig, dpi=dpi, bbox_inches='tight')

    clf = kwargs.get('clf', bool(show) or bool(savefig))
    if clf:
        plt.clf()
def Set(ax=None, **kwargs):
    axesDict = dict()
    axisDict = dict()
    figDict = dict()
    for key, value in kwargs.items():
        if key in axesKey:
            axesDict[key] = value
        elif key in axisKey:
            axisDict[key] = value
        elif key in figKey:
            figDict[key] = value
        else:
            print(f'[Warning] {key} has not define, please check!')
    SetAxes(ax, **axesDict)
    SetAxis(ax, **axisDict)
    SetFig(**figDict)

# Common Function
def KwargsGet(kwargs, key, default, reserve:bool=False):
    if reserve:
        return kwargs.get(key, default)
    else:
        try:
            return kwargs.pop(key)
        except KeyError:
            return default

# Draw Image
def CDF(series, ax=None, **kwargs):
    """
    :param kwargs: legend:None
    :return:
    """
    data = np.sort(series)
    length = len(data)
    cdf = np.linspace(0, 1, length)

    ax = plt.gca() if ax==None else ax
    ax.plot(data, cdf, label=kwargs.get('legend', None))

    kwargs['yticks'] = kwargs.get('yticks', ([0.1 * i for i in range(11)], [f'{10 * i}%' for i in range(11)]))
    Set(ax, **kwargs)

def PDF(series, ax=None, **kwargs):
    """
    :param kwargs: legend:None
    :return:
    """
    series = np.sort(series)
    value = np.unique(series)
    pdf = np.bincount(series)
    pdf = pdf[np.where(pdf!=0)] / np.sum(pdf)

    ax = plt.gca() if ax == None else ax
    ax.plot(value, pdf, label=kwargs.get('legend', None))

    Set(ax, **kwargs)

def Scatter(x, y, ax=None,**kwargs):
    """
    :param kwargs:  color:None, legend:None, trendLine:True, polyFit:1, annotate:False
    """
    count = 100
    expandRate = 0.05
    vmin, vmax = np.min(x), np.max(x)
    xn = np.linspace((1+expandRate)*vmin-expandRate*vmax, (1+expandRate)*vmax-expandRate*vmin, count)

    color = KwargsGet(kwargs, 'color', None, False)
    legend = KwargsGet(kwargs, 'legend', None, True)
    ax = plt.gca() if ax == None else ax
    ax.scatter(x, y, s=5, color=color, label=legend)
    if KwargsGet(kwargs, 'trendLine', True, False):
        polyFit = KwargsGet(kwargs, 'polyFit', 1, False)
        if polyFit in kwargs.keys():
            del kwargs['polyFit']
        z = np.polyfit(x, y, polyFit)
        p = np.poly1d(z)
        ax.plot(xn, p(xn), color=color)

        if KwargsGet(kwargs, 'annotate', False, False):
            formula = f'f(X) = {z[0]:.2f}*X{polyFit}'
            for i in range(polyFit):
                formula += f' + {z[i+1]:.2f}*X{polyFit-i-1}'
            formula = formula[:-3]
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            formula = f'{formula}\nR2 = {r_value ** 2:.3f}'
            ax.annotate(formula, xy=(vmin, p(vmin)))

    Set(ax, **kwargs)

def Histograms(series, ax=None, **kwargs):
    """
    :param kwargs: vmin, vmax, step
    :return:
    """
    vmin = KwargsGet(kwargs, 'vmin', np.min(series), False)
    vmax = KwargsGet(kwargs, 'vmax', np.man(series), False)
    step = KwargsGet(kwargs, 'step', (vmax-vmin)/20, False)
    bins = np.arange(vmin-step/2, vmax+step/2, step)

    ax = plt.gca() if ax == None else ax
    ax.hist(series, bins)

    Set(**kwargs)

def Boxplot(df, ax=None, **kwargs):
    columns = df.columns.to_list()
    kwargs['xticks'] = ([i + 1 for i in range(len(columns))], columns)

    ax = plt.gca() if ax == None else ax
    ax.boxplot(df)

    Set(ax, **kwargs)

if __name__ == '__main__':
    # plt.plot([1, 2, 3, 4], [1, 2, 3, 4])
    # SetAxes(xticks=((1, 2, 3, 4), ('a', 'b', 'c', 'd')), grid=True)
    # plt.show()

    x = np.random.randint(0, 100, 1000)
    y = np.random.randint(0, 100, 1000)
    Scatter(x, y, show=True)