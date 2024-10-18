import tkinter as tk
from tkinter import ttk
import database, message
import re, math


def NamingRule(name:str)->bool:
    if type(name) != str:
        return False
    if len(name) <= 0:
        return False
    if not bool(re.fullmatch('[a-zA-Z0-9_]+', name)):
        return False
    if name[0].isdigit():
        return False
    return True

def AddColumn(root):
    """
    numList = [i for i in '0123456789']
    symbol = [i for i in '+-*/^%√']
    bracket = ['(', ')']
    :param root:
    :return:
    """
    def on_select(event):
        column = f'data[\'{comboColumn.get()}\']'
        current = strVar.get()
        obj = re.match("^(.*)data\['\w+'\]$", current)
        if len(current) == 0:
            strVar.set(column)
        elif obj:
            current = obj.group(1)
            strVar.set(f'{current}{column}')
        elif current[-1] in [i for i in '+-*/^%(']:
            strVar.set(f'{current}{column}')
        elif current[-1] in [i for i in '0123456789√)']:
            pass
        else:
            pass
    def InsertNum(num):
        current = strVar.get()
        if len(current) == 0:
            if num != 0:
                strVar.set(f'{num}')
        elif current[-1] in [i for i in '0123456789']:
            strVar.set(f'{current}{num}')
        elif current[-1] in [i for i in '+-*/^%(']:
            if num == 0:
                return
            strVar.set(f'{current}{num}')
        elif current[-1] in [i for i in '√)']:
            pass
        else:
            pass
    def InsertSymbol(symbol):
        current = strVar.get()
        if len(current) == 0:
            if symbol == '√':
                strVar.set(symbol)
        elif current[-1] in [i for i in '0123456789']:
            if symbol != '√':
                strVar.set(f'{current}{symbol}')
        elif current[-1] in [i for i in '+-*/^%']:
            if symbol != '√':
                strVar.set(f'{current[:-1]}{symbol}')
            else:
                strVar.set(f'{current}{symbol}')
        elif current[-1] == ']':
            if symbol != '√':
                strVar.set(f'{current}{symbol}')
        elif current[-1] == '√':
            pass
        elif current[-1] == '(':
            if symbol == '√':
                strVar.set(f'{current}{symbol}')
        elif current[-1] == ')':
            if symbol != '√':
                strVar.set(f'{current}{symbol}')
    def InsertBracket(bracket):
        current = strVar.get()
        if len(current) == 0:
            if bracket == '(':
                strVar.set('(')
        elif current[-1] in [i for i in '0123456789)]']:
            if bracket == ')':
                strVar.set(f'{current}{bracket}')
        elif current[-1] in [i for i in '+-*/^%√(']:
            if bracket == '(':
                strVar.set(f'{current}{bracket}')
        else:
            pass
    def AddCol(root_t):
        newColName = colName.get()
        strFunc = '0' if strVar.get() == '' else strVar.get()
        if not NamingRule(newColName):
            message.ShowNormalWarn('new column name do not match naming rule!')
            return
        zBracketCnt = 0
        fBracketCnt = 0
        for c in strFunc:
            if c == '(':
                zBracketCnt += 1
            elif c == ')':
                fBracketCnt += 1
            if zBracketCnt < fBracketCnt:
                message.ShowNormalWarn('pls check bracket')
                return
        if zBracketCnt != fBracketCnt:
            message.ShowNormalWarn('pls check bracket')
            return
        strFunc = strFunc.replace('^', '**')
        strFunc = strFunc.replace('√', 'math.sqrt')
        try:
            database.data[newColName] = database.data.apply(lambda data:eval(strFunc), axis=1)
        except Exception:
            message.ShowNormalWarn('formula has error, pls check')
            return
        root_t.destroy()
    if not database.CheckData():
        return
    size = 10
    columns = database.data.columns.tolist()

    root_t = tk.Toplevel(root)
    strVar = tk.StringVar()
    colName = tk.StringVar()
    colName.set('Fill_New_Col_name')
    comboColumn = ttk.Combobox(root_t, width=15)
    comboColumn['values'] = tuple(columns)
    comboColumn.bind('<<ComboboxSelected>>', on_select)
    comboColumn.grid(row=1, column=5)
    tk.Entry(root_t, textvariable=strVar, state='readonly', width=3*size+1).grid(row=0, column=0, columnspan=5)
    tk.Entry(root_t, textvariable=colName, width=18).grid(row=0, column=5, columnspan=5)
    tk.Button(root_t, text=' 1 ', padx=size, command=lambda:InsertNum(1)).grid(row=1, column=0)
    tk.Button(root_t, text=' 2 ', padx=size, command=lambda:InsertNum(2)).grid(row=1, column=1)
    tk.Button(root_t, text=' 3 ', padx=size, command=lambda:InsertNum(3)).grid(row=1, column=2)
    tk.Button(root_t, text=' + ', padx=size, command=lambda:InsertSymbol('+')).grid(row=1, column=3)
    tk.Button(root_t, text=' ^ ', padx=size, command=lambda:InsertSymbol('^')).grid(row=1, column=4)

    tk.Button(root_t, text=' 4 ', padx=size, command=lambda:InsertNum(4)).grid(row=2, column=0)
    tk.Button(root_t, text=' 5 ', padx=size, command=lambda:InsertNum(5)).grid(row=2, column=1)
    tk.Button(root_t, text=' 6 ', padx=size, command=lambda:InsertNum(6)).grid(row=2, column=2)
    tk.Button(root_t, text=' - ', padx=size, command=lambda:InsertSymbol('-')).grid(row=2, column=3)
    tk.Button(root_t, text=' √ ', padx=size, command=lambda:InsertSymbol('√')).grid(row=2, column=4)

    tk.Button(root_t, text=' 7 ', padx=size, command=lambda:InsertNum(7)).grid(row=3, column=0)
    tk.Button(root_t, text=' 8 ', padx=size, command=lambda:InsertNum(8)).grid(row=3, column=1)
    tk.Button(root_t, text=' 9 ', padx=size, command=lambda:InsertNum(9)).grid(row=3, column=2)
    tk.Button(root_t, text=' * ', padx=size, command=lambda:InsertSymbol('*')).grid(row=3, column=3)
    tk.Button(root_t, text=' % ', padx=size, command=lambda:InsertSymbol('%')).grid(row=3, column=4)

    tk.Button(root_t, text=' ( ', padx=size, command=lambda:InsertBracket('(')).grid(row=4, column=0)
    tk.Button(root_t, text=' 0 ', padx=size, command=lambda:InsertNum(0)).grid(row=4, column=1)
    tk.Button(root_t, text=' ) ', padx=size, command=lambda:InsertBracket(')')).grid(row=4, column=2)
    tk.Button(root_t, text=' / ', padx=size, command=lambda:InsertSymbol('/')).grid(row=4, column=3)
    tk.Button(root_t, text='// ', padx=size, command=lambda:InsertSymbol('//')).grid(row=4, column=4)

    tk.Button(root_t, text='Reset', padx=25, pady=5, command=lambda:strVar.set('')).grid(row=2, column=5)
    tk.Button(root_t, text='Entry', padx=25, pady=12, command=lambda:AddCol(root_t)).grid(row=3, column=5, rowspan=2)

def DelColumn(root):
    def RunDelColumn(valueList):
        columns = database.data.columns.tolist()
        for index, value in enumerate(valueList):
            if value.get():
                database.data.drop(columns[index], axis=1, inplace=True)
        root_t.destroy()
    if not database.CheckData():
        return
    root_t = tk.Toplevel(root)
    tk.Label(root_t, text='选择需要删除的Column,\n再 按“Delete” 删除').pack()
    columns = database.data.columns.tolist()
    valueList = []
    for column in columns:
        boolValue = tk.BooleanVar()
        boolValue.set(False)
        checkButton = tk.Checkbutton(root_t, text=column, variable=boolValue)
        checkButton.pack()
        valueList.append(boolValue)
    button = tk.Button(root_t, text='Delete Column', command=lambda:RunDelColumn(valueList))
    button.pack()

def SelColumn(root):
    def RunSelColumn(valueList):
        columns = database.data.columns.tolist()
        for index, value in enumerate(valueList):
            if not value.get():
                database.data.drop(columns[index], axis=1, inplace=True)
        root_t.destroy()

    if not database.CheckData():
        return
    root_t = tk.Toplevel(root)
    tk.Label(root_t, text='选择需要保留的Column,\n再 按“Start” 运行').pack()
    columns = database.data.columns.tolist()
    valueList = []
    for column in columns:
        boolValue = tk.BooleanVar()
        boolValue.set(False)
        checkButton = tk.Checkbutton(root_t, text=column, variable=boolValue)
        checkButton.pack()
        valueList.append(boolValue)
    button = tk.Button(root_t, text='Start', command=lambda: RunSelColumn(valueList))
    button.pack()

def RenameColumn(root):
    def Run():
        if newName.get() in columns:
            return
        index = columns.index(oldName.get())
        columns[index] = newName.get()
        database.data.columns = columns
        comboColumn['values'] = tuple(columns)
    def Quit():
        root_t.destroy()
    def on_select(event):
        oldName.set(comboColumn.get())
    oldName = tk.StringVar()
    newName = tk.StringVar()
    root_t = tk.Toplevel(root)
    columns = database.data.columns.tolist()
    comboColumn = ttk.Combobox(root_t, width=15)
    comboColumn['values'] = tuple(columns)
    comboColumn.bind('<<ComboboxSelected>>', on_select)
    comboColumn.grid(row=1, column=0)
    newName.set('New_Name')
    tk.Entry(root_t, textvariable=newName).grid(row=1, column=1)
    tk.Button(root_t, text='run', command=Run, width=10).grid(row=2, column=0)
    tk.Button(root_t, text='quit', command=Quit, width=10).grid(row=2, column=1)

    # root_t.destroy()




if __name__ == '__main__':
    # df = pd.read_excel(r'H:\Python\UI_DataAnalysis\other\temp.xlsx', header=0)
    # print(df)
    # df['num'] = df.apply(lambda df:1, axis=1)
    # print(df)

    print(math.sqrt(10))