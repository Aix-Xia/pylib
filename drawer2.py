import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LogNorm
import numpy as np
from scipy.stats import linregress


GnRd1 = colors.LinearSegmentedColormap.from_list('rgy', [(0.0, (0.0, 1.0, 0.0)), (0.5, (1.0, 1.0, 0.0)), (1.0, (1.0, 0.0, 0.0))])
GnRd2 = colors.LinearSegmentedColormap.from_list('rgy', [(0.0, (1.0, 0.0, 0.0)), (0.5, (1.0, 1.0, 0.0)), (1.0, (0.0, 1.0, 0.0))])

# plt figure Setting
dpi = 600
axesKey = ('title', 'grid', 'legend',
           'xticks', 'xlabel', 'xscale', 'axhline', 'xlim', 'xrotation',
           'yticks', 'ylabel', 'yscale', 'axvline', 'ylim', 'yrotation')
axisKey = ('right', 'left', 'top', 'bottom')
figKey = ('suptitle', 'show', 'savefig', 'clf')
colorBarKey = ('cbar', 'cticks')
def SetAxes(ax=None, **kwargs):
    """
    :param ax:
    :param kwargs:  title, grid, legend
                    xticks, xlabel, xscale, axhline, xlim, xrotation
                    yticks, ylabel, yscale, axvline, ylim, yrotation
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
    xrotation = kwargs.get('xrotation', 0)
    if xticks:
        xtickList, xlabelList = GetTicksAndLabels(xticks)
        ax.set_xticks(xtickList, xlabelList, rotation=xrotation)

    yticks = kwargs.get('yticks', None)
    yrotation = kwargs.get('yrotation', 0)
    if yticks:
        ytickList, ylabelList = GetTicksAndLabels(yticks)
        ax.set_yticks(ytickList, ylabelList, rotation=yrotation)

    axvline = kwargs.get('axvline', None)
    if axvline != None:
        if type(axvline) in (int, float):
            ax.axvline(axvline, linestyle="--", color="k", lw=0.5)
        elif type(axvline) in (list, tuple, set):
            for x in axvline:
                ax.axvline(x, linestyle="--", color="k", lw=0.5)
        else:
            raise(TypeError(f'{type(axvline)} has not define'))

    axhline = kwargs.get('axhline', None)
    if axhline != None:
        if type(axhline) in (int, float):
            ax.axhline(axhline, linestyle="--", color="k", lw=0.5)
        elif type(axhline) in (list, tuple, set):
            for y in axhline:
                ax.axhline(y, linestyle="--", color="k", lw=0.5)
        else:
            raise(TypeError(f'{type(axhline)} has not define'))

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
        ax.grid(which='both')

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

    clf = kwargs.get('clf', bool(savefig))
    if clf:
        plt.clf()
def SetColorBar(image, **kwargs):
    cbar = KwargsGet(kwargs, 'cbar', False, False)
    cticks = KwargsGet(kwargs, 'cticks', None, False)
    if cbar or cticks:
        colorbar = plt.colorbar(image)
        if cticks == None:
            return
        ctickList, clabelList = GetTicksAndLabels(cticks)
        colorbar.set_ticks(ctickList)
        colorbar.set_ticklabels(clabelList)

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
def GetTicksAndLabels(ticks):
    if type(ticks) not in [tuple, list]:
        raise (TypeError('ticks must tuple or list type'))
    tickList = []
    labelList = []
    allNum = True
    for tick in ticks:
        if type(tick) not in (float, int):
            tickList = []
            labelList = []
            allNum = False
            break
        else:
            tickList.append(tick)
            labelList.append(str(tick))
    if not allNum:
        if len(ticks) < 2:
            raise (ValueError('cticks has error'))
        if len(ticks[0]) != len(ticks[1]):
            raise (ValueError('cticks length has error'))
        for i in range(len(ticks[0])):
            if type(ticks[0][i]) not in (int, float):
                raise (ValueError('ytick value has error'))
            tickList.append(ticks[0][i])
            labelList.append(str(ticks[1][i]))
    return tickList, labelList

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

    trendLine = KwargsGet(kwargs, 'trendLine', None, False)
    if trendLine == 'linear':
        polyFit = 1
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
    elif trendLine == None:
        pass
    else:
        print('[Warning] %s(trendLine) has not define, please check!!'%trendLine)

    Set(ax, **kwargs)

def Histograms(series, ax=None, **kwargs):
    """
    :param kwargs: vmin, vmax, step
    :return:
    """
    vmin = KwargsGet(kwargs, 'vmin', np.min(series), False)
    vmax = KwargsGet(kwargs, 'vmax', np.max(series), False)
    step = KwargsGet(kwargs, 'step', (vmax-vmin)/30, False)
    bins = np.arange(vmin-step/2, vmax+step/2, step)

    ax = plt.gca() if ax == None else ax
    label = KwargsGet(kwargs, 'legend', None, True)
    alpha = KwargsGet(kwargs, 'alpha', 1, False)
    ax.hist(series, bins, label=label, alpha=alpha)

    Set(**kwargs)

def BoxPlot(df, ax=None, **kwargs):
    columns = df.columns.to_list()
    kwargs['xticks'] = ([i + 1 for i in range(len(columns))], columns)

    ax = plt.gca() if ax == None else ax
    ax.boxplot(df)

    Set(ax, **kwargs)

def HeatMap(df, ax=None, **kwargs):
    """
    :param kwargs: aspect:1, vmaxRed:True, vmin:None, vmax:None, scale:'linear', cbar:False, cticks:None
    :return:
    """
    # ysize, xsize = df.shape
    aspect = KwargsGet(kwargs, 'aspect', 1, False) * df.shape[1] / df.shape[0]
    GnRd = GnRd1 if KwargsGet(kwargs, 'vmaxRed', True, False) else GnRd2

    vmin = KwargsGet(kwargs, 'vmin', None, False)
    vmax = KwargsGet(kwargs, 'vmax', None, False)
    vmin = (df.min() if (type(df) == np.ndarray) else df.min().min()) if (vmin == None) else vmin
    vmax = (df.max() if (type(df) == np.ndarray) else df.max().max()) if (vmax == None) else vmax

    axvline = KwargsGet(kwargs, 'axvline', None, True)
    if axvline:
        kwargs['axvline'] = [i - 0.5 for i in axvline]
    axhline = KwargsGet(kwargs, 'axhline', None, True)
    if axhline:
        kwargs['axhline'] = [i - 0.5 for i in axhline]

    # 画 heat map
    ax = plt.gca() if ax == None else ax
    scale = KwargsGet(kwargs, 'scale', 'linear', False)
    if scale == 'log':
        if vmax <= 0:
            raise (ValueError('vmax can not less than 0 then scale is log'))
        elif vmin <= 0:
            vmin = min(vmax / 100, 0.9)
        p = ax.imshow(df, norm=LogNorm(vmin=vmin, vmax=vmax), cmap=GnRd, aspect=aspect, interpolation='nearest')
    elif scale == 'linear':
        p = ax.imshow(df, cmap=GnRd, vmin=vmin, vmax=vmax, aspect=aspect, interpolation='nearest')
    else:
        raise(ValueError(f'{scale} has not define'))

    # setting color bar
    cbar = KwargsGet(kwargs, 'cbar', False, False)
    cticks = KwargsGet(kwargs, 'cticks', None, False)
    SetColorBar(p, cbar=cbar, cticks=cticks)
    Set(ax, **kwargs)


if __name__ == '__main__':
    # plt.plot([1, 2, 3, 4], [1, 2, 3, 4])
    # SetAxes(xticks=((1, 2, 3, 4), ('a', 'b', 'c', 'd')), grid=True)
    # plt.show()

    x = np.random.randint(0, 100, 1000)
    y = np.random.randint(0, 100, 1000)
    Scatter(x, y, show=True)