from tkinter import messagebox


def ShowFileTypeErrorWarn():
    messagebox.showwarning('警告', '尚未定义读取该格式文件')
def ShowDataNoneWarn():
    messagebox.showwarning('警告', '数据尚未导入')
def ShowDataLoadErrorWarn():
    messagebox.showwarning('警告', '数据导入错误')
def ShowNormalWarn(text):
    messagebox.showwarning('警告', text)
def ShowInfo(s:str):
    messagebox.showinfo('Info', s)



if __name__ == '__main__':
    ShowInfo('sfsfda')