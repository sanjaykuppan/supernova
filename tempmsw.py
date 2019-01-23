import pandas as pd
import os.path
from tkinter import *
from tkinter import messagebox


#Main stock window
def msw():
    pop=Tk()
    pop.title("Super Nova")
    pop.geometry("900x650")
    pop.attributes("-fullscreen",False)
    B1=Button(pop,text="Stock I/P",command = AddStock)
    B1.place(x=500,y=100)
    B2=Button(pop,text="Stock Correction",command= StockCorrect)
    B2.place(x=500,y=150)
    B3=Button(pop,text="Stock Detail",command = StockDetail)
    B3.place(x=500,y=200)
    B4=Button(pop,text="View Product file",command = ViewProduct)
    B4.place(x=500,y=250)
    B5=Button(pop,text="Add Product", command = AddProduct)
    B5.place(x=500,y=300)
    #Definiton to exit Full Screen
    def FullScreen():
        if (pop.attributes("-fullscreen")):
            pop.attributes("-fullscreen",False)
        else:
            pop.attributes("-fullscreen",True)
        return
    B6=Button(pop,text="Full screen On/OFF",command = FullScreen)
    B6.place(x=850,y=10)
    pop.mainloop()

#Definiton to add stock to MSF
def AddStock():
    return

#Definiton to correct stock in MSF
def StockCorrect():
    return
    
#Definiton to get available stock detail
def StockDetail():
    return
#Definiton to view PCF
def ViewProduct():
    return
#Definiton to add product to PCF
def AddProduct():
    return


    
msw()
