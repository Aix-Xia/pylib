import pandas as pd
import message
import tkinter as tk
from tkinter import ttk


filePath = ''
# data = None
data = pd.read_excel(r'H:\Python\UI_DataAnalysis\other\temp.xlsx', sheet_name=0)
sheetIndex = 0
headerRow = 0


def CheckData():
    if type(data) != pd.core.frame.DataFrame:
        message.ShowDataLoadErrorWarn()
        return False
    return True

def Stack(root):
    def DataStack():
        global data
        unstackColumnList = []
        columns = data.columns.tolist()
        for column in columns:
            if column not in stackColumnList:
                unstackColumnList.append(column)
        if len(unstackColumnList) == 0:
            root_t.destroy()
            return
        data.set_index(keys=unstackColumnList, drop=True, inplace=True)
        data = data.stack().reset_index()
        data.columns = unstackColumnList + [stackLabelVar.get(), stackDataVar.get()]
        root_t.destroy()
    def SelectReset():
        length = len(stackColumnList)
        for i in range(length):
            stackColumnList.pop()
        dispalyString.set('')
    def on_select(event):
        column = comboColumn.get()
        if column not in stackColumnList:
            stackColumnList.append(column)
            s = ''
            for col in stackColumnList:
                s = s + col + ', '
            s = s[:-2]
            dispalyString.set(s)
    stackColumnList = []
    columns = data.columns.tolist()
    # root_t = tk.Tk()
    root_t = tk.Toplevel(root)

    tk.Label(root_t, text='Stack Column List    : ').grid(row=0, column=0)
    tk.Label(root_t, text='Need Add Stack Column: ').grid(row=1, column=0)
    dispalyString = tk.StringVar()
    display = tk.Entry(root_t, textvariable=dispalyString, state='readonly')
    display.grid(row=0, column=1)

    comboColumn = ttk.Combobox(root_t)
    comboColumn['values'] = tuple(columns)
    comboColumn.bind('<<ComboboxSelected>>', on_select)
    comboColumn.grid(row=1, column=1)

    stackLabelVar = tk.StringVar()
    stackLabelVar.set('Label')
    stackDataVar = tk.StringVar()
    stackDataVar.set('Data')
    tk.Label(root_t, text='Stack Label Name     : ').grid(row=2, column=0)
    tk.Label(root_t, text='Stack Data Name      : ').grid(row=3, column=0)
    tk.Entry(root_t, textvariable=stackLabelVar).grid(row=2, column=1)
    tk.Entry(root_t, textvariable=stackDataVar).grid(row=3, column=1)

    tk.Button(root_t, text='Stack', command=DataStack).grid(row=4, column=0)
    tk.Button(root_t, text='Reset', command=SelectReset).grid(row=4, column=1)

    # root_t.mainloop()

def Pivot():
    def run():
        global data
        data = data.pivot_table(index=comboIndex.get(), columns=comboColumn.get(), values=comboData.get(), aggfunc=comboFunc.get())
        root_t.destroy()
    if not CheckData():
        return
    columns = data.columns.tolist()
    root_t = tk.Tk()
    tk.Label(root_t, text='index  : ').grid(row=0, column=0)
    tk.Label(root_t, text='column : ').grid(row=1, column=0)
    tk.Label(root_t, text='data   : ').grid(row=2, column=0)
    tk.Label(root_t, text='aggfunc: ').grid(row=3, column=0)
    comboIndex = ttk.Combobox(root_t)
    comboIndex['values'] = tuple(columns)
    # comboIndex.bind('<<ComboboxSelected>>', on_select)
    comboIndex.grid(row=0, column=1)
    comboColumn = ttk.Combobox(root_t)
    comboColumn['values'] = tuple(columns)
    # comboIndex.bind('<<ComboboxSelected>>', on_select)
    comboColumn.grid(row=1, column=1)
    comboData = ttk.Combobox(root_t)
    comboData['values'] = tuple(columns)
    # comboIndex.bind('<<ComboboxSelected>>', on_select)
    comboData.grid(row=2, column=1)
    comboFunc = ttk.Combobox(root_t)
    comboFunc['values'] = ('mean', 'sum', 'count')
    comboFunc.set('mean')
    # comboIndex.bind('<<ComboboxSelected>>', on_select)
    comboFunc.grid(row=3, column=1)

    tk.Button(root_t, text='Pivot', command=run).grid(row=4, column=0, columnspan=2)

    root_t.mainloop()


def ResetData():
    global data
    if filePath == '':
        message.ShowNormalWarn('没有初始化数据')
    if filePath.endswith('.csv'):
        data = pd.read_csv(filePath, header=headerRow)
    elif filePath.endswith('.xls') or filePath.endswith('.xlsx'):
        data = pd.read_excel(filePath, sheet_name=sheetIndex, header=headerRow)
    else:
        message.ShowFileTypeErrorWarn()

if __name__ == '__main__':
    data = pd.read_excel(r'H:\Python\UI_DataAnalysis\other\temp.xlsx', sheet_name=0)