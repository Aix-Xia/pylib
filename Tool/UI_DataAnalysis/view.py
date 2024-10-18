import tkinter as tk
from tkinter import ttk
import database


def ShowDataFrame(df, root):
    # columns = df.columns.tolist()
    # # 创建Tkinter窗口
    # root_t = tk.Tk()
    # # 创建Treeview小部件
    # tree = ttk.Treeview(root_t, columns=columns, show='headings')
    # # 设置列的标题
    # for column in columns:
    #     tree.heading(column, text=column)
    # # 插入数据
    # for index, row in df.iterrows():
    #     tree.insert('', 'end', text=index, values=row.tolist())
    # # 布局Treeview小部件
    # tree.pack(fill=tk.BOTH, expand=True)
    # # 启动Tkinter时间循环
    # root_t.mainloop()
    columns = df.columns.tolist()
    # 创建Tkinter窗口
    root_t = tk.Toplevel(root)
    # 创建Treeview小部件
    tree = ttk.Treeview(root_t, columns=[' '] + columns, show='headings')
    # 设置列的标题
    for column in [' '] + columns:
        tree.heading(column, text=column)
    # 插入数据
    for index, row in df.iterrows():
        tree.insert('', 'end', text=index, values=[index] + row.tolist())
    # 布局Treeview小部件
    tree.pack(fill=tk.BOTH, expand=True)
    # 启动Tkinter时间循环
    # root_t.mainloop()
def ShowInfo(root):
    if not database.CheckData():
        return
    shape = database.data.shape
    columns = database.data.columns.tolist()
    index = database.data.index.tolist()
    columns = columns if (len(columns) <= 4) else (columns[:4] + ['···'])
    index = columns if (len(index) <= 4) else (index[:4] + ['···'])
    root_t = tk.Toplevel(root)
    # root_t.geometry('300x200+50+50')  # 'WidthxHeight+X+Y'
    root_t.resizable(True, True)
    tk.Label(root_t, text=f'xSize = {shape[1]}\n', font=('Times', 16), anchor='w').pack()
    tk.Label(root_t, text=f'ySize = {shape[0]}\n', font=('Times', 16), anchor='w').pack()
    tk.Label(root_t, text=f'index = {index}\n', font=('Times', 16), anchor='w').pack()
    tk.Label(root_t, text=f'columns = {columns}\n', font=('Times', 16), anchor='w').pack()


def ShowData(root):
    if not database.CheckData():
        return
    ShowDataFrame(database.data, root)
def ShowColumn(root):
    if not database.CheckData():
        return
    columns = database.data.columns
    root_t = tk.Toplevel(root)
    for column in columns:
        tk.Button(root_t, text=column, font=('宋体', 12), width=12, height=1).pack()
def ShowDescribe(root):
    if not database.CheckData():
        return
    df = database.data.describe()
    # df.columns = ['describe'] + df.columns.tolist()[1:]
    ShowDataFrame(df, root)