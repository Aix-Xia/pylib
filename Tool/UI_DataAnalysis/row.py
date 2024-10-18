import message, database
import tkinter as tk
import pandas as pd


def AddRow(root):
    def Add():
        newRow = [eval(rowString.get() if rowString.get() != '' else 'numpy.NaN') for rowString in rowList]
        database.data.loc[database.data.shape[0]] = newRow
    def Quit(root_t):
        root_t.destroy()
    root_t = tk.Toplevel(root)
    columns = database.data.columns.tolist()
    rowList = []
    index = 0
    for column in columns:
        var = tk.StringVar()
        rowList.append(var)
        tk.Label(root_t, text=column + ' : ').grid(row=index, column=0)
        tk.Entry(root_t, textvariable=var).grid(row=index, column=1)
        index += 1
    tk.Button(root_t, text='Add', command=Add).grid(row=index, column=0)
    tk.Button(root_t, text='Quit', command=lambda:Quit(root_t)).grid(row=index, column=1)

def DelRow(root):
    message.ShowNormalWarn('has not development!')

def RenameRow(root):
    message.ShowNormalWarn('has not development!')


if __name__ == '__main__':
    df = pd.DataFrame({'A':[1, 2, 3], 'B':[4, 5, 6]})
    # print(df.shape[0])
    df.loc[df.shape[0]] = [11, 12]
    print(df)