import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from scipy.stats import linregress


numTypeNameSet = ('int', 'float') + tuple(f'int{2**i}' for i in range(3, 7)) + tuple(f'float{2**i}' for i in range(4, 7))
iterTypeNameSet = ('Series', 'ndarray', 'list', 'tuple', 'set')


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
        if type(axvline).__name__ in numTypeNameSet:
            ax.axvline(axvline, linestyle="--", color="k", lw=0.5)
        elif type(axvline).__name__ in iterTypeNameSet:
            for x in axvline:
                ax.axvline(x, linestyle="--", color="k", lw=0.5)
        else:
            raise(TypeError(f'{type(axvline)} has not define'))

    axhline = kwargs.get('axhline', None)
    if axhline != None:
        if type(axhline).__name__ in numTypeNameSet:
            ax.axhline(axhline, linestyle="--", color="k", lw=0.5)
        elif type(axhline).__name__ in iterTypeNameSet:
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


# color map
class COLOR:
    def __init__(self, r, g, b, v=0.0):
        self.r = r
        self.g = g
        self.b = b
        self.v = v
    def __str__(self):
        return f'[{self.v}:({self.r}, {self.g}, {self.b})]'
    def __call__(self, value):
        self.v = value
        return self
    @staticmethod
    def __SetData(value):
        if type(value).__name__ not in numTypeNameSet:
            raise(TypeError('input data must "int" or "float"!'))
        elif value < 0 or value > 1:
            raise(ValueError('input data is out of limit!'))
        else:
            return value
    def __SetR(self, value):
        self.__r = COLOR.__SetData(value)
    def __SetG(self, value):
        self.__g = COLOR.__SetData(value)
    def __SetB(self, value):
        self.__b = COLOR.__SetData(value)
    def __SetV(self, value):
        self.__v = COLOR.__SetData(value)
    r = property(lambda self:self.__r, __SetR, lambda self:None)
    g = property(lambda self:self.__g, __SetG, lambda self:None)
    b = property(lambda self:self.__b, __SetB, lambda self:None)
    v = property(lambda self:self.__v, __SetV, lambda self:None)
    @classmethod
    @property
    def red(cls):
        return COLOR(1, 0, 0)
    @classmethod
    @property
    def yellow(cls):
        return COLOR(1, 1, 0)
    @classmethod
    @property
    def green(cls):
        return COLOR(0, 1, 0)
    @classmethod
    @property
    def blue(cls):
        return COLOR(0, 0, 1)
def CreateColorMap(lowColor:COLOR, highColor:COLOR, *args:COLOR):
    lowColor.v = 0.0
    highColor.v = 1.0
    colorList = [lowColor, highColor] + list(filter(lambda c:((c.v != 0) or (c.v != 1)), args))
    colorList = sorted(colorList, key=lambda i:i.v)
    cd = {'red':[],
          'green':[],
          'blue':[]}
    for color in colorList:
        cd['red'].append((color.v, color.r, color.r))
        cd['green'].append((color.v, color.g, color.g))
        cd['blue'].append((color.v, color.b, color.b))
    cmap = mcolors.LinearSegmentedColormap('LogColorMap', cd)
    return cmap


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
    if type(ticks).__name__ not in iterTypeNameSet:
        raise (TypeError('ticks must tuple or list type'))
    tickList = []
    labelList = []
    allNum = True
    for tick in ticks:
        if type(tick).__name__ not in numTypeNameSet:
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
            if type(ticks[0][i]).__name__ not in numTypeNameSet:
                raise (ValueError('ytick value has error'))
            tickList.append(ticks[0][i])
            labelList.append(str(ticks[1][i]))
    return tickList, labelList
def GetAxes(ax=None):
    if ax==None:
        return plt.gca()
    elif type(ax).__name__ == 'Axes':
        raise(TypeError('ax must be type "Axes"'))
    else:
        return ax
def GetArray2D(data)->np.ndarray:
    if type(data).__name__ == 'DataFrame':
        data = data.values
    elif type(data).__name__ == 'ndarray':
        pass
    else:
        raise(TypeError(f'df type is {type(data).__name__} that has not define!'))
    return data

# Draw Image
def CDF(series, ax=None, **kwargs):
    """
    :param kwargs: legend:None
    :return:
    """
    data = np.sort(series)
    length = len(data)
    cdf = np.linspace(0, 1, length)

    ax = GetAxes(ax)
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

    ax = GetAxes(ax)
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

    size = KwargsGet(kwargs, 'size', 5, False)
    color = KwargsGet(kwargs, 'color', None, False)
    legend = KwargsGet(kwargs, 'legend', None, True)
    ax = GetAxes(ax)
    ax.scatter(x, y, s=size, color=color, label=legend)

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

    ax = GetAxes(ax)
    label = KwargsGet(kwargs, 'legend', None, True)
    alpha = KwargsGet(kwargs, 'alpha', 1, False)
    ax.hist(series, bins, label=label, alpha=alpha)

    Set(**kwargs)

def BoxPlot(df, ax=None, **kwargs):
    columns = df.columns.to_list()
    kwargs['xticks'] = ([i + 1 for i in range(len(columns))], columns)

    ax = GetAxes(ax)
    ax.boxplot(df)

    Set(ax, **kwargs)

def Bar(df, ax=None, **kwargs):
    ax = GetAxes(ax)
    axis = KwargsGet(kwargs, 'axis', 0, False)
    if axis==1:
        df = df.T
    xlabel = df.index.to_list()
    xticks = np.arange(len(xlabel))
    width = 0.75 / df.shape[1]

    size = KwargsGet(kwargs, 'fontsize', 8, False)
    color = KwargsGet(kwargs, 'fontcolor', 'black', False)
    label = KwargsGet(kwargs, 'datalabel', False, False)
    for index, column in enumerate(df.columns):
        rect = ax.bar(xticks + index * width, df[column], width, label=column)
        if label:
            ax.bar_label(rect, size=size, color=color)

    kwargs['xticks'] = ([tick + width * (df.shape[1] - 1) / 2 for tick in xticks], xlabel)
    Set(ax, **kwargs)

def HeatMap(df, ax=None, **kwargs):
    """
    :param kwargs: aspect:1, vmaxRed:True, vmin:None, vmax:None, scale:'linear', cbar:False, cticks:None
    :return:
    """
    df = GetArray2D(df)
    ysize, xsize = df.shape
    aspect = KwargsGet(kwargs, 'aspect', 1, False) * xsize / ysize
    vmaxRed = KwargsGet(kwargs, 'vmaxRed', True, False)

    axvline = KwargsGet(kwargs, 'axvline', None, True)
    if axvline:
        kwargs['axvline'] = [i - 0.5 for i in axvline]
    axhline = KwargsGet(kwargs, 'axhline', None, True)
    if axhline:
        kwargs['axhline'] = [i - 0.5 for i in axhline]

    # 画 heat map
    ax = GetAxes(ax)
    scale = KwargsGet(kwargs, 'scale', 'linear', False)
    if scale == 'linear':
        vmin = KwargsGet(kwargs, 'vmin', np.nanmin(df), False)
        vmedian = KwargsGet(kwargs, 'vmedian', np.nanmedian(df), False)
        vmax = KwargsGet(kwargs, 'vmax', np.nanmax(df), False)
        rate = (vmedian - vmin) / (vmax - vmin)
        # cmap = CreateColorMap(COLOR.green if vmaxRed else COLOR.red,
        #                       COLOR.red if vmaxRed else COLOR.green,
        #                       COLOR.yellow(rate))
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    elif scale == 'log':
        vmin = KwargsGet(kwargs, 'vmin', np.nanmin(df[df > 0]), False)
        vmedian = KwargsGet(kwargs, 'vmedian', np.nanmedian(df[df > 0]), False)
        vmax = KwargsGet(kwargs, 'vmax', np.nanmax(df[df > 0]), False)
        rate = (np.log2(vmedian) - np.log2(vmin)) / (np.log2(vmax) - np.log2(vmin))
        # cmap = CreateColorMap(COLOR.green if vmaxRed else COLOR.red,
        #                       COLOR.red if vmaxRed else COLOR.green,
        #                       COLOR.yellow(rate))
        norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
    else:
        raise(ValueError(f'{scale} has not define'))
    if vmaxRed:
        lc = COLOR.green
        hc = COLOR.red
    else:
        lc = COLOR.red
        hc = COLOR.green
    mc = COLOR.yellow(rate)
    cmap = CreateColorMap(lc, hc, mc)
    image = ax.imshow(df, cmap=cmap, norm=norm, aspect=aspect, interpolation='nearest')

    # setting color bar
    cbar = KwargsGet(kwargs, 'cbar', False, False)
    cticks = KwargsGet(kwargs, 'cticks', None, False)
    SetColorBar(image, cbar=cbar, cticks=cticks)
    Set(ax, **kwargs)

def Text(df, ax=None, **kwargs):
    ax = GetAxes(ax)
    size = KwargsGet(kwargs, 'fontsize', 8, False)
    color = KwargsGet(kwargs, 'fontcolor', 'black', False)

    ysize, xsize = df.shape
    for irow in range(ysize):
        for icol in range(xsize):
            try:
                data = df.values[irow, icol]
            except Exception:
                data = df[irow, icol]
            if not np.isnan(data):
                value = f'{data:.1e}'
                ax.text(icol, irow, value, horizontalalignment='center', verticalalignment='center',
                        fontdict={'fontsize': size, 'color': color, 'weight': 'bold', 'family': 'Times New Roman'})

if __name__ == '__main__':
    pass