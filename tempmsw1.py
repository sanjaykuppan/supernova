import pandas as pd
import os.path
from tkinter import *
from tkinter import messagebox
import workproduct as wp #import work product box


class MSW:
    #Definiton to check existence PCF file 
    def checkfile(self,fname):
        if(os.path.isfile(fname)):
            return True
        return False
    #Definition to add Stock to MSF
    def AddStock(self):
        return
    #Definiton to correct stock in MSF
    def StockCorrect(self):
        return
    #Definiton to get available stock detail
    def StockDetail(self):
        return
    #Definiton to view PCF
    def ViewProduct(self):
        if(self.checkfile('pcf.csv')):
            wp.ViewProductFile()
            return
        else:
            messagebox.showinfo(title="No file exists",message='Product file not found')
            return
    #Definiton to add product to PCF
    def AddProduct(self):
        if(self.checkfile('pcf.csv')):
            wp.addproduct()
            return
        else:
            df=pd.DataFrame(columns=['code','name','company','GST%','category'])
            df.to_csv('pcf.csv',index=False)
            messagebox.showinfo(title='No File exists',message='New File created')
            return

#Main stock window
def mswd():
    msw1=MSW()
    box=Tk()
    box.title("Super Nova")
    box.geometry("900x650")
    box.attributes("-fullscreen",False)
    B1=Button(box,text="Stock I/P",command = msw1.AddStock())
    B1.place(x=500,y=100)
    B2=Button(box,text="Stock Correction",command= msw1.StockCorrect)
    B2.place(x=500,y=150)
    B3=Button(box,text="Stock Detail",command = msw1.StockDetail)
    B3.place(x=500,y=200)
    B4=Button(box,text="View Product file",command = msw1.ViewProduct)
    B4.place(x=500,y=250)
    B5=Button(box,text="Add Product", command = msw1.AddProduct)
    B5.place(x=500,y=300)
    #Definiton to exit Full Screen
    def FullScreen():
        if (box.attributes("-fullscreen")):
            box.attributes("-fullscreen",False)
        else:
            box.attributes("-fullscreen",True)
        return
    B6=Button(box,text="Full screen On/OFF",command = FullScreen)
    B6.place(x=850,y=10)
    def close():
        box.destroy()
        return
    B7=Button(box,text="  Exit  ",command = close)
    B7.place(x=850,y=600)
    box.mainloop()

#First call Definition
mswd()
