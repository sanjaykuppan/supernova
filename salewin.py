from tkinter import *
from tkinter import messagebox
import sqlite3
import workdb as wdb
import saleview
import os.path
import fileexport as fexpo

class salewindow:
    def checkfile(self,fname):
        if(os.path.isfile(fname)):
            return True
        return False
    #View sales file
    def Viewsales(self,w):
        if self.checkfile('msw.db'):
            saleview.sale()
            return
        else:
            messagebox.showinfo(parent=w,title='File not found',message='Database file not found!!')
            return
    def export(self):
        if self.checkfile('msw.db'):
            fexpo.exportfile()
            return
        else:
            messagebox.showinfo(parent=w,title='File not found',message='Database file not found!!!')
        return


#sale window definition
def salewin():
    saw=salewindow()
    salebox=Toplevel()
    salebox.title("Sales Window")
    salebox.geometry("900x650")
    img=PhotoImage(file='saleswindow.png')
    L=Label(salebox,image=img)
    L.pack(side='top',pady=50)
    Bv=Button(salebox,text='View sales file',command=lambda w=salebox:saw.Viewsales(w))
    Bv.pack(side='top',pady=10)
    Be=Button(salebox,text='Export to file',command=saw.export)
    Be.pack(side='top',pady=0)
    def ex():
        salebox.destroy()
    Ex=Button(salebox,text='Exit',command=ex)
    Ex.pack(side='top',pady=10)
    salebox.mainloop()
#salewin()
