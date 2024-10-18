import pandas as pd
import tkinter as tk
from tkinter import filedialog
import message, database



def LoadDataFromFile(root):
    def runCsv(root_t):
        try:
            database.headerRow = None if (headerStr.get() < 1) else (headerStr.get() - 1)
        except Exception:
            message.ShowNormalWarn('pls key in integer data')
            return
        root_t.destroy()
        database.ResetData()
    def runExcel(root_t):
        try:
            database.sheetIndex = sheetStr.get() - 1
            database.headerRow = None if (headerStr.get() < 1) else (headerStr.get() - 1)
        except Exception:
            message.ShowNormalWarn('pls key in integer data')
            return
        root_t.destroy()
        database.ResetData()
    database.filePath = filedialog.askopenfilename()
    root_t = tk.Toplevel(root)
    if database.filePath.endswith('.csv'):
        tk.Label(root_t, text='header_row').grid(row=0, column=0)
        headerStr = tk.IntVar()
        headerStr.set(1)
        tk.Entry(root_t, textvariable=headerStr).grid(row=0, column=1)
        tk.Button(root_t, text='run', command=lambda:runCsv(root_t), width=15).grid(row=1, column=0, columnspan=2)
    elif database.filePath.endswith('.xls') or database.filePath.endswith('.xlsx'):
        tk.Label(root_t, text='sheet_index').grid(row=0, column=0)
        sheetStr = tk.IntVar()
        sheetStr.set(1)
        tk.Entry(root_t, textvariable=sheetStr).grid(row=0, column=1)
        tk.Label(root_t, text='header_row').grid(row=1, column=0)
        headerStr = tk.IntVar()
        headerStr.set(1)
        tk.Entry(root_t, textvariable=headerStr).grid(row=1, column=1)
        tk.Button(root_t, text='run', command=lambda:runExcel(root_t), width=15).grid(row=2, column=0, columnspan=2)
def ClearData():
    database.filePath = ''
    database.data = None
def SaveData():
    file_path = filedialog.asksaveasfilename(initialfile='unknow.csv', filetypes=[('file', '.csv')])
    database.data.to_csv(file_path, header=True, index=False)

def QuitSoftWare(root):
    root.quit()


if __name__ == '__main__':
    path_csv = r'G:\Test\temp\macro00_cycle02_n1.csv'
    path_excel = r'G:\Test\temp\macro00_cycle02_n1.xlsx'
    # df_csv = pd.read_csv(path_csv, header=2, index_col=4)
    df_excel = pd.read_excel(path_excel, sheet_name=0, header=None, index_col=10)
    # print(df_csv)
    print(df_excel)