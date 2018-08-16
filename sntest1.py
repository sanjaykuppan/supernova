import os.path
import tkinter.font as font
from tkinter import *
from tkinter import messagebox
import sqlite3
import stockwin as stk
import salewin as sale
import billwin as bill
import returnwin as ret

class MasterWindow:
    #Definition for work on MSF
    def MasterStock(self):
        stk.stockwin()
        return
    #Definiton for Billing
    def Billing(self,box):
        if os.path.isfile("MSW.db"):
            bill.MainWindow()
            return
        else:
            messagebox.showinfo(parent=box,title="Error",message="Database file not found!!")
            return
    #Definiton for return product
    def ReturnProduct(self):
        if os.path.isfile("MSW.db"):
            ret.returnwin()
            return
        else:
            messagebox.showinfo(parent=box,title="Error",message="Database file not found!!")                     
        return
    #Definiton for sales file
    def SalesFile(self):
        if os.path.isfile("MSW.db"):
            sale.salewin()
            return
        else:
            messagebox.showinfo(parent=box,title="Error",message="Database file not found!!!")
        return


#Main window
def MainWindow():
    mw1=MasterWindow()
    box=Tk()
    box.title("Super Nova")
    box.state('zoomed')
    box.attributes("-fullscreen",False)
    photo=PhotoImage(file='MW.png')
    LT=Label(box,image=photo)
    LT.place(x=400,y=50)
    B1=Button(box,text="Work with Master Stock File",command = mw1.MasterStock,font='Times')
    B1.place(x=500,y=200)
    B2=Button(box,text="Billing",command=lambda box=box:mw1.Billing(box),font='Times')
    B2.place(x=500,y=250)
    B3=Button(box,text="Return",command = mw1.ReturnProduct,font='Times')
    B3.place(x=500,y=300)
    B4=Button(box,text="Sales File",command = mw1.SalesFile,font='Times')
    B4.place(x=500,y=350)
    #Definiton to exit Full Screen
    def FullScreen():
        if (box.attributes("-fullscreen")):
            box.attributes("-fullscreen",False)
        else:
            box.attributes("-fullscreen",True)
        return
    BFS=Button(box,text="Full screen On/OFF",command = FullScreen)
    BFS.place(x=950,y=10)
    def close():
        box.destroy()
        return
    BE=Button(box,text="  Exit  ",command = close)
    BE.place(x=850,y=650)
    box.mainloop()

#First call Definition
MainWindow()

