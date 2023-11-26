# encoding: UTF-8

# from tkinter import *
import  windnd
import tkinter
from tkinter import filedialog

from tkinter.messagebox import showinfo


# import filedialogs
# from filedialogs import *


def inputnumber():
    print(123)
    # filedialog.Directory
    b = tkinter.filedialog.askdirectory()
    print(b)

def dragged_files(files):

    msg = '\n'.join((item.decode('gbk') for item in files))
    showinfo("拖拽文件路径",msg)

root = tkinter.Tk()

b = tkinter.Button(root, text="open", fg="red", command=inputnumber).grid(row=0, column=0)
windnd.hook_dropfiles(root , func=dragged_files)

root.mainloop()
