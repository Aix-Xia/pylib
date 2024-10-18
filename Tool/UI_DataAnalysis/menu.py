import tkinter as tk
import file, view, column, row, database, analysis



def EditMenuFile(root, menu_bar):
    # 添加file一级菜单
    file_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label='File', menu=file_menu)
    # 添加下拉菜单
    file_menu.add_command(label='Load Data', command=lambda: file.LoadDataFromFile(root))
    file_menu.add_command(label='Clear Data', command=file.ClearData)
    file_menu.add_separator()
    file_menu.add_command(label='Save as', command=file.SaveData)
    file_menu.add_separator()
    file_menu.add_command(label='Quit', command=lambda: file.QuitSoftWare(root))
def EditMenuView(root, menu_bar):
    # 添加view一级菜单
    view_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label='view', menu=view_menu)
    # 添加下拉菜单
    view_menu.add_command(label='Info', command=lambda: view.ShowInfo(root))
    view_menu.add_command(label='Describe', command=lambda: view.ShowDescribe(root))
def EditMenuData(root, menu_bar):
    # 添加view一级菜单
    data_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label='data', menu=data_menu)
    # 添加下拉菜单
    data_menu.add_command(label='Show', command=lambda: view.ShowData(root))
    data_menu.add_separator()
    data_menu.add_command(label='Stack', command=lambda : database.Stack(root))
    data_menu.add_command(label='Pivot', command=database.Pivot)
    data_menu.add_separator()
    data_menu.add_command(label='Reset Data', command=database.ResetData)
def EditMenuColumn(root, menu_bar):
    # 添加column一级菜单
    edit_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label='Column', menu=edit_menu)
    # 添加下拉菜单
    edit_menu.add_command(label='Show', command=lambda: view.ShowColumn(root))
    edit_menu.add_separator()
    edit_menu.add_command(label='Add', command=lambda: column.AddColumn(root))
    edit_menu.add_command(label='Delete', command=lambda: column.DelColumn(root))
    edit_menu.add_command(label='Select', command=lambda: column.SelColumn(root))
    edit_menu.add_command(label='Rename', command=lambda: column.RenameColumn(root))
def EditMenuRow(root, menu_bar):
    # 添加row一级菜单
    edit_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label='Row', menu=edit_menu)
    # 添加下拉菜单
    edit_menu.add_command(label='Add', command=lambda: row.AddRow(root))
    edit_menu.add_command(label='Delete', command=lambda: row.DelRow(root))
    edit_menu.add_command(label='Rename', command=lambda: row.RenameRow(root))
def EditMenuAnalysis(root, menu_bar):
    # 添加help一级菜单
    analysis_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label='Analysis', menu=analysis_menu)
    # 添加下拉菜单
    analysis_menu.add_command(label='Fit Y with X', command=lambda: analysis.FitXWithY(root))
    analysis_menu.add_command(label='CDF', command=lambda: analysis.CDF(root))
    analysis_menu.add_command(label='Distribution', command=lambda: analysis.Distribution(root))
    analysis_menu.add_command(label='Heat Map', command=lambda: analysis.HeatMap(root))

def EditMenuHelp(root, menu_bar):
    # 添加help一级菜单
    help_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(label='Help', menu=help_menu)
    # 添加下拉菜单


def CreateMenu(root):
    # 创建菜单栏
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    EditMenuFile(root, menu_bar)
    EditMenuView(root, menu_bar)
    EditMenuData(root, menu_bar)
    EditMenuColumn(root, menu_bar)
    EditMenuRow(root, menu_bar)
    EditMenuAnalysis(root, menu_bar)
    EditMenuHelp(root, menu_bar)

if __name__ == '__main__':
    data = database.data.describe().reset_index()
    data.columns = ['describe'] + data.columns.tolist()[1:]

    print(data)