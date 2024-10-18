import tkinter as tk
import menu



def main():
    root = tk.Tk()
    root.title('Data Analysis')
    root.geometry('800x600+50+50')  # 'WidthxHeight+X+Y'
    root.resizable(True, True)

    menu.CreateMenu(root)

    root.mainloop()


if __name__ == '__main__':
    main()