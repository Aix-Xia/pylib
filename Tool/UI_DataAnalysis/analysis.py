import database, message
import math
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LogNorm

GnRd1 = colors.LinearSegmentedColormap.from_list('rgy', [(0.0, (0.0, 1.0, 0.0)), (0.5, (1.0, 1.0, 0.0)), (1.0, (1.0, 0.0, 0.0))])
GnRd2 = colors.LinearSegmentedColormap.from_list('rgy', [(0.0, (1.0, 0.0, 0.0)), (0.5, (1.0, 1.0, 0.0)), (1.0, (0.0, 1.0, 0.0))])

def HeatMap(root):
    def Drawer():
        GnRd = GnRd1 if comboColorScheme.get() == 'Green << Red' else GnRd2
        scale = comboColorScale.get()
        ysize, xsize = database.data.shape
        xyrate = 1  # 1.4

        if ysize < 10:
            yticks = [i for i in range(ysize)]
        else:
            yticks = [i for i in range(0, ysize, math.ceil(ysize / 10))]

        if xsize < 10:
            xticks = [i for i in range(xsize)]
        else:
            xticks = [i for i in range(0, xsize, math.ceil(xsize / 10))]

        try:
            xline = eval(xlist.get())
        except Exception:
            xline = list(map(lambda i: 'None' if i.strip(' ') == '' else i.strip(' '), xlist.get().split(',')))
            xline = list(filter(lambda i:type(eval(i)) in (int, float), xline))
        try:
            yline = eval(ylist.get())
        except Exception:
            yline = list(map(lambda i: 'None' if i.strip(' ') == '' else i.strip(' '), ylist.get().split(',')))
            yline = list(filter(lambda i: type(eval(i)) in (int, float), yline))

        limit = (eval(llimit.get()) if llimit.get()!='' else '', eval(hlimit.get()) if hlimit.get()!='' else '')
        if (type(limit[0]) not in (int, float)) or (type(limit[1]) not in (int, float)):
            limit = None
        if limit == None:
            vmin = database.data.min().min()
            vmax = database.data.max().max()
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
            cticks = [i for i in range(int(vmin), int(vmax) + 1, math.ceil((vmax - vmin) / 10 + 1))]
        else:
            raise (ValueError(f'{scale} has not define'))

        fig, ax = plt.subplots()
        if scale == 'log':
            p = ax.imshow(database.data, norm=LogNorm(vmin=vmin, vmax=vmax), cmap=GnRd, aspect=xyrate * xsize / ysize, interpolation='nearest')
        elif scale == 'linear':
            p = ax.imshow(database.data, cmap=GnRd, vmin=vmin, vmax=vmax, aspect=xyrate * xsize / ysize, interpolation='nearest')
        else:
            raise (ValueError(f'{scale} has not define'))
        cbar = fig.colorbar(p, ax=ax)
        cbar.set_ticks(cticks)
        cbar.set_ticklabels([str(tick) for tick in cticks])

        plt.yticks([tick for tick in yticks], [str(tick) for tick in yticks])
        if type(yline) == list:
            for i in yline:
                plt.axhline(y=i + 0.5, linestyle="--", color="k", lw=0.5)

        plt.xticks([tick for tick in xticks], [str(tick) for tick in xticks], rotation=-60)
        if type(xline) == list:
            for i in xline:
                plt.axvline(x=i + 0.5, linestyle="--", color="k", lw=0.5)
        # plt.imshow(database.data)
        plt.show()

    labelList = ['Color Scheme', 'Color Bar Scale', 'Color Bar Lower Limit', 'Color Bar High Limit', 'X Line List', 'Y Line List']
    scaleList = ['log', 'linear']
    schemeList = ['Green << Red', 'Red << Green']
    llimit = tk.StringVar()
    llimit.set(str(database.data.min().min()))
    hlimit = tk.StringVar()
    hlimit.set(str(database.data.max().max()))
    xlist = tk.StringVar()
    ylist = tk.StringVar()

    root_t = tk.Toplevel(root)
    index = 0
    for label in labelList:
        tk.Label(root_t, text=label).grid(row=index, column=0)
        index += 1

    comboColorScheme = ttk.Combobox(root_t, width=15)
    comboColorScheme['values'] = schemeList
    comboColorScheme.set(schemeList[0])
    comboColorScheme.bind('<<ComboboxSelected>>', lambda event:None)
    comboColorScheme.grid(row=0, column=1)

    comboColorScale = ttk.Combobox(root_t, width=15)
    comboColorScale['values'] = scaleList
    comboColorScale.set(scaleList[1])
    comboColorScale.bind('<<ComboboxSelected>>', lambda event: None)
    comboColorScale.grid(row=1, column=1)

    tk.Entry(root_t, textvariable=llimit).grid(row=2, column=1)
    tk.Entry(root_t, textvariable=hlimit).grid(row=3, column=1)

    tk.Entry(root_t, textvariable=xlist).grid(row=4, column=1)
    tk.Entry(root_t, textvariable=ylist).grid(row=5, column=1)

    tk.Button(root_t, text='Drawer', command=Drawer).grid(row=index, column=0)
    tk.Button(root_t, text='Quit', command=lambda:root_t.destroy()).grid(row=index, column=1)


def FitXWithY(root):
    def on_select(event):
        pass
    def XFitY():
        xColumn = comboColumnX.get()
        yColumn = comboColumnY.get()
        if xColumn and yColumn:
            plt.scatter(database.data[xColumn], database.data[yColumn], label=None if label.get() == '' else label.get())

            xScale = comboColumnXS.get()
            plt.xscale(xScale)
            yScale = comboColumnYS.get()
            plt.yscale(yScale)

            xl = xllimit.get()
            xh = xhlimit.get()
            if xl != '' and xh != '':
                xl = eval(xl)
                xh = eval(xh)
                if (type(xl) not in (int, float)) or (type(xh) not in (int, float)):
                    message.ShowNormalWarn('X limit fill error!')
                    return
                plt.xlim(xl, xh)
            yl = yllimit.get()
            yh = yhlimit.get()
            if yl != '' and yh != '':
                yl = eval(yl)
                yh = eval(yh)
                if (type(yl) not in (int, float)) or (type(yh) not in (int, float)):
                    message.ShowNormalWarn('Y limit fill error!')
                    return
                plt.xlim(yl, yh)
            plt.legend()
            plt.show()
        else:
            message.ShowNormalWarn('has not select columns')
    columns = database.data.columns.tolist()
    scaleList = ('log', 'linear')
    label = tk.StringVar()

    root_t = tk.Toplevel(root)
    tk.Entry(root_t, textvariable=label).grid(row=0, column=0)
    tk.Label(root_t, text='Select Column').grid(row=0, column=1)
    tk.Label(root_t, text='Select Scale').grid(row=0, column=2)
    tk.Label(root_t, text='lower Limit').grid(row=0, column=3)
    tk.Label(root_t, text='high Limit').grid(row=0, column=4)

    tk.Label(root_t, text='X Axis Information : ').grid(row=1, column=0)
    tk.Label(root_t, text='Y Axis Information : ').grid(row=2, column=0)

    comboColumnX = ttk.Combobox(root_t, width=15)
    comboColumnX['values'] = tuple(columns)
    comboColumnX.bind('<<ComboboxSelected>>', on_select)
    comboColumnX.grid(row=1, column=1)
    comboColumnY = ttk.Combobox(root_t, width=15)
    comboColumnY['values'] = tuple(columns)
    comboColumnY.bind('<<ComboboxSelected>>', on_select)
    comboColumnY.grid(row=2, column=1)

    comboColumnXS = ttk.Combobox(root_t, width=15)
    comboColumnXS['values'] = scaleList
    comboColumnXS.set(scaleList[1])
    comboColumnXS.bind('<<ComboboxSelected>>', on_select)
    comboColumnXS.grid(row=1, column=2)
    comboColumnYS = ttk.Combobox(root_t, width=15)
    comboColumnYS['values'] = scaleList
    comboColumnYS.set(scaleList[1])
    comboColumnYS.bind('<<ComboboxSelected>>', on_select)
    comboColumnYS.grid(row=2, column=2)

    xllimit = tk.StringVar()
    xhlimit = tk.StringVar()
    yllimit = tk.StringVar()
    yhlimit = tk.StringVar()
    tk.Entry(root_t, textvariable=xllimit).grid(row=1, column=3)
    tk.Entry(root_t, textvariable=yllimit).grid(row=2, column=3)
    tk.Entry(root_t, textvariable=xhlimit).grid(row=1, column=4)
    tk.Entry(root_t, textvariable=yhlimit).grid(row=2, column=4)

    tk.Button(root_t, text='Drawer Image', command=XFitY).grid(row=3, column=0, columnspan=5)


def Distribution(root):
    message.ShowNormalWarn('has not development!')

def CDF(root):
    def OnSelect(event):
        ll = database.data[comboData.get()].min()
        hl = database.data[comboData.get()].max()
        llimit.set(ll)
        hlimit.set(hl)
    def Imshow():
        if not comboData.get():
            message.ShowNormalWarn('data can not None!')
            return
        if comboGroup.get():
            _label = label.get() + '_' if label.get() else ''
            for key, df in database.data.groupby(by=comboGroup.get()):
                s = df[comboData.get()].to_frame('col')
                s = s.dropna()['col']
                s = list(s.sort_values())
                length = len(s)
                cdf = [100 * i / (length - 1) for i in range(length)]
                plt.plot(s, cdf, label=_label+str(key))
        else:
            _label = label.get()
            s = database.data[comboData.get()].to_frame('col')
            s = s.dropna()['col']
            s = list(s.sort_values())
            length = len(s)
            cdf = [100 * i / (length - 1) for i in range(length)]
            plt.plot(s, cdf, label=_label)
        plt.xscale(comboScale.get())
        ll = llimit.get()
        hl = hlimit.get()
        if ll and hl:
            ll = eval(ll)
            hl = eval(hl)
            if (type(ll) not in (float, int)) or (type(hl) not in (float, int)):
                pass
            else:
                plt.xlim(ll, hl)
        plt.legend()
        plt.show()

    # message.ShowNormalWarn('has not development!')
    columns = database.data.columns.tolist()
    scaleTuple = ('log', 'linear')
    root_t = tk.Toplevel(root)
    index = 0
    label = tk.StringVar()
    llimit = tk.StringVar()
    hlimit = tk.StringVar()

    for value in ['Label : ', 'Data : ', 'Group : ', 'Scale : ', 'Low Limit : ', 'Hign Limit : ']:
        tk.Label(root_t, text=value).grid(row=index, column=0)
        index += 1
    tk.Entry(root_t, textvariable=label).grid(row=0, column=1)
    comboData = ttk.Combobox(root_t, width=15)
    comboData['values'] = columns
    comboData.bind('<<ComboboxSelected>>', OnSelect)
    comboData.grid(row=1, column=1)
    comboGroup = ttk.Combobox(root_t, width=15)
    comboGroup['values'] = [''] + columns
    comboGroup.bind('<<ComboboxSelected>>', lambda event:None)
    comboGroup.grid(row=2, column=1)
    comboScale = ttk.Combobox(root_t, width=15)
    comboScale['values'] = scaleTuple
    comboScale.set(scaleTuple[1])
    comboScale.bind('<<ComboboxSelected>>', lambda event:None)
    comboScale.grid(row=3, column=1)
    tk.Entry(root_t, textvariable=llimit).grid(row=4, column=1)
    tk.Entry(root_t, textvariable=hlimit).grid(row=5, column=1)
    tk.Button(root_t, text='Drawer', command=Imshow).grid(row=index, column=0)
    tk.Button(root_t, text='Quit', command=lambda:root_t.destroy()).grid(row=index, column=1)




if __name__ == '__main__':
    a = (1, 2, 3)
    b = (4, 5, 6)
    print(a + b)