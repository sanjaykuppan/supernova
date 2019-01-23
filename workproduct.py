from tkinter import *
from tkinter import messagebox
import pandas as pd
from pandastable import Table, TableModel

#Add product main definition
def addproduct():    
    ent=Tk()#main add product window
    ent.geometry("800x600")
    ent.title('Product input')
    ent.lift()
    def Val(ins,maxlen,value):#parameters(is input made,max lenght,
        maxlen=int(maxlen)
        if ins =='1' :#check insert true
            if not len(value)<maxlen:
                return False 
        return True
    E1=Entry(ent,text="Product code",bd=10,validate="key",width=5)
    E1['validatecommand']=(E1.register(Val),'%d',6,'%P')
    E1.place(x=250,y=50)
    L1=Label(ent,text="Enter Product code")
    L1.place(x=85,y=50)
    E2=Entry(ent,text="Product Name",bd=10,validate="key",width=25)
    E2['validatecommand']=(E2.register(Val),'%d',26,'%P')
    E2.place(x=250,y=150)
    L2=Label(ent,text="Enter Product Name")
    L2.place(x=85,y=150)
    E3=Entry(ent,text="Company",bd=10,validate="key",width=25)
    E3['validatecommand']=(E3.register(Val),'%d',26,'%P')
    E3.place(x=250,y=250)
    L3=Label(ent,text="Enter Company Name")
    L3.place(x=85,y=250)
    E4=Entry(ent,text="GST %",bd=10,validate='key',width=5)
    E4['validatecommand']=(E4.register(Val),'%d',6,'%P')
    E4.place(x=250,y=350)
    L4=Label(ent,text="Enter GST %")
    L4.place(x=85,y=350)
    E5=Entry(ent,text="Category",bd=10,validate='key',width=20)
    E5['validatecommand']=(E5.register(Val),'%d',21,'%P')
    E5.place(x=250,y=450)
    L5=Label(ent,text="Enter Category")
    L5.place(x=85,y=450)
    #Definiton to check and add value to pcf file
    def AddCheck():
        if E1.get() and E2.get() and E3.get() and E4.get() and E5.get():
            v1=E1.get().upper()
            v2=E2.get().upper()
            v3=E3.get().upper()
            v4=E4.get()
            v5=E5.get().upper()
            try:
                v4=float(v4)
                if not v4<28:
                    print (1/0)
            except:
                messagebox.showinfo(title='WrongValue',message="Enter Correct GST value")
                ent.lift()
                return
            df=pd.DataFrame(columns=[v1,v2,v3,v4,v5])
            df.to_csv('pcf.csv',index=False,mode="a")
            messagebox.showinfo(title="Sucess",message="Product added Successfully")
            E1.delete(0,'end')
            E2.delete(0,'end')
            E3.delete(0,'end')
            E4.delete(0,'end')
            E5.delete(0,'end')
            ent.lift()
            return
        else:
            messagebox.showinfo(title="Value Required",message="Enter All Value")
            ent.lift()
            return

        return
    B1=Button(ent,text="Add Product",command=AddCheck)
    B1.place(x=550,y=200)
    def close():
        ent.destroy()
        return 
    B2=Button(ent,text="  Exit  ",command= close)
    B2.place(x=560,y=250)
    ent.mainloop()
    return

#View Product file Main definiton
def ViewProductFile():
    df=pd.read_csv('pcf.csv')
    vbox=Tk()
    vbox.geometry("800x600")
    vbox.title("Product File")
    f=Frame(vbox)
    f.pack(fill=BOTH,expand=1)
    pt=Table(f,dataframe=df)
    pt.show()
    return
