import os.path
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import workdb as wdb
import datetime
import json
import getstoredata as gstrdata

class stockwindow:
    def checkfile(self,fname):
        if(os.path.isfile(fname)):
            return True
        return False
    #add stock window
    def addstock(self,w):
        ent=Toplevel(master=w)#main add product window
        ent.geometry("800x600")
        ent.title('Product input')
        ent.lift()
        def Val(ins,maxlen,value):#parameters(is input made,max lenght,
            maxlen=int(maxlen)
            if ins =='1' :#check insert true
                if not len(value)<maxlen:
                    return False 
            return True
        def block(ins):    
            if ins=='1' or ins=='0':
                return False
            elif ins=='-1':
                return True
        def intval(ins,maxlen,value):
            try:
                val=int(value)    
                maxlen=int(maxlen)
                if ins=='1':
                    if not ((isinstance(val,int) and len(value)<maxlen)):
                        return False
                return True
            except:
                if not len(value)==0:
                    return False
                return True
        def floatval(ins,maxlen,value):
            try:
                val=float(value)
                maxlen=int(maxlen)
                if ins=='1':
                    if not((isinstance(val,float) and len(value)<maxlen)):
                        return False
                return True
            except:
                if not len(value)==0:
                    return False
                return True
        #Item type array is fetched from storedetail.json file.
        if os.path.isfile("storedetail.json"):
            a=os.path.abspath(os.getcwd())+"\storedetail.json"
            f=open(a)
            data=json.load(f)
            itype=data["itemtype"]
        else:
            itype=[]
        E1=Entry(ent,text="ITEM CODE",bd=10,validate="key",width=5)
        E1['validatecommand']=(E1.register(intval),'%d',6,'%P')
        E1.place(x=200,y=50)
        L1=Label(ent,text="Enter Item code")
        L1.place(x=25,y=50)
        Li=Label(ent,text="Item Type")
        Li.place(x=300,y=50)
        Ei=ttk.Combobox(ent,width=20,values=itype,validate='key')
        Ei.place(x=380,y=50)
        Ei['validatecommand']=(Ei.register(block),'%d')
        E2=Entry(ent,text="stock i/p invoice Number",bd=10,validate="key",width=20)
        E2['validatecommand']=(E2.register(Val),'%d',20,'%P')
        E2.place(x=200,y=100)
        L2=Label(ent,text="Enter Invoice Number")
        L2.place(x=25,y=100)
        E3=Entry(ent,text="Company",bd=10,validate="key",width=25)
        E3['validatecommand']=(E3.register(Val),'%d',26,'%P')
        E3.place(x=200,y=150)
        L3=Label(ent,text="Enter Dealer Name")
        L3.place(x=25,y=150)
        E4=Entry(ent,text="Description",bd=10,validate='key',width=30)
        E4['validatecommand']=(E4.register(Val),'%d',18,'%P')
        E4.place(x=200,y=200)
        L4=Label(ent,text="Enter Product Description")
        L4.place(x=25,y=200)
        E5=Entry(ent,text="HSN code",bd=10,validate='key',width=8)
        E5['validatecommand']=(E5.register(intval),'%d',9,'%P')
        E5.place(x=200,y=250)
        L5=Label(ent,text="Enter HSN code")
        L5.place(x=25,y=250)
        L6=Label(ent,text="Enter Manufacturing Date")
        L6.place(x=25,y=320)
        E6d=Entry(ent,text="MFG Date DD",bd=10,validate='key',width=2)
        E6d['validatecommand']=(E6d.register(intval),'%d',3,'%P')
        E6d.place(x=200,y=320)
        L6d=Label(ent,text="DD")
        L6d.place(x=200,y=295)
        E6m=Entry(ent,text="MFG Date MM",bd=10,validate='key',width=2)
        E6m['validatecommand']=(E6d.register(intval),'%d',3,'%P')
        E6m.place(x=230,y=320)
        L6m=Label(ent,text="MM")
        L6m.place(x=230,y=295)
        E6y=Entry(ent,text="MFG Date YYYY",bd=10,validate='key',width=4)
        E6y['validatecommand']=(E6d.register(intval),'%d',5,'%P')
        E6y.place(x=260,y=320)
        L6y=Label(ent,text="YYYY")
        L6y.place(x=260,y=295)
        L7=Label(ent,text="Enter Expiry Date")
        L7.place(x=25,y=360)
        E7d=Entry(ent,text="EXP Date DD",bd=10,validate='key',width=2)
        E7d['validatecommand']=(E6d.register(intval),'%d',3,'%P')
        E7d.place(x=200,y=360)
        E7m=Entry(ent,text="EXP Date MM",bd=10,validate='key',width=2)
        E7m['validatecommand']=(E6d.register(intval),'%d',3,'%P')
        E7m.place(x=230,y=360)
        E7y=Entry(ent,text="EXP Date YYYY",bd=10,validate='key',width=4)
        E7y['validatecommand']=(E6d.register(intval),'%d',5,'%P')
        E7y.place(x=260,y=360)
        E8=Entry(ent,text="GST%(CGST+SGST)",bd=10,validate='key',width=5)
        E8['validatecommand']=(E8.register(floatval),'%d',5,'%P')
        E8.place(x=200,y=410)
        L8=Label(ent,text="Enter GST%(CGST+SGST) ")
        L8.place(x=25,y=410)
        E9=Entry(ent,text="Price(Without GST)",bd=10,validate='key',width=6)
        E9['validatecommand']=(E8.register(floatval),'%d',7,'%P')
        E9.place(x=200,y=460)
        L9=Label(ent,text="Price per unit(Without GST)")
        L9.place(x=25,y=460)
        E10=Entry(ent,text="Units",bd=10,validate='key',width=6)
        E10['validatecommand']=(E8.register(intval),'%d',6,'%P')
        E10.place(x=200,y=510)
        L10=Label(ent,text="No. of units")
        L10.place(x=25,y=510)
        vr=StringVar(value="Kgs")
        R1=Radiobutton(ent,text="Pcs",variable=vr,value="Pcs")
        R1.place(x=250,y=520)
        R2=Radiobutton(ent,text="Kgs",variable=vr,value="Kgs")
        R2.place(x=300,y=520)
        #Definiton to check and add value to pcf file
        def AddCheck():
            a=E1.get() and E2.get() and E3.get() and E4.get() and E5.get() and E8.get() and E9.get() and E10.get() and Ei.get()
            b=E6d.get() and E6m.get() and E6y.get() and E7d.get() and E7m.get() and E7y.get()
            if a and b:
                try:
                    v1=E1.get()#itemcode
                    v2=E2.get()#invoice number
                    v3=(E3.get()).upper()#Dealer name
                    v4=(str(E4.get())).upper()#Description
                    v5=E5.get()#HSN
                    v6d=int(E6d.get())#MFG
                    v6m=int(E6m.get())
                    v6y=int(E6y.get())
                    v7d=int(E7d.get())#EXP
                    v7m=int(E7m.get())
                    v7y=int(E7y.get())
                    v8=float(E8.get())#GST
                    vmd=str(v6y)+'-'+str(v6m)+'-'+str(v6d)#MFG date
                    ved=str(v7y)+'-'+str(v7m)+'-'+str(v7d)#EXP date
                    v9=E9.get()#Price
                    v10=E10.get()#units
                    v11=Ei.get()#item type
                    vr1=(vr.get()).upper()#utype
                    try:
                        datetime.date(v6y,v6m,v6d)
                        datetime.date(v7y,v7m,v7d)
                        if not datetime.date(v6y,v6m,v6d)<datetime.date.today() or not datetime.date(v7y,v7m,v7d)>datetime.date.today():
                            print (1/0)
                    except:
                        messagebox.showinfo(parent=ent,title="Wrong Date",message="Enter correct date")
                        end.lift()
                        return
                    if not v8<28:
                        messagebox.showinfo(parent=ent,title='WrongValue',message="Enter Correct GST value")
                        print (1/0)
                except:
                    ent.lift()
                    return
                try:
                    con=sqlite3.connect('MSW.db')
                    con.execute("""insert into stock (Itemcode,Description,HSN,MFG,EXP,GST,Dealer,InvoiceNumber,Price,Units,Utype,Itemtype) values(?,?,?,?,?,?,?,?,?,?,?,?);""",(v1,v4,v5,vmd,ved,v8,v3,v2,v9,v10,vr1,v11))
                    con.commit()
                    con.close()
                    messagebox.showinfo(parent=ent,title="Sucess",message="Product added Successfully")
                    E1.delete(0,'end')
                    E2.delete(0,'end')
                    E3.delete(0,'end')
                    E4.delete(0,'end')
                    E5.delete(0,'end')
                    E6d.delete(0,'end')
                    E6m.delete(0,'end')
                    E6y.delete(0,'end')
                    E7d.delete(0,'end')
                    E7m.delete(0,'end')
                    E7y.delete(0,'end')
                    E8.delete(0,'end')
                    E9.delete(0,'end')
                    E10.delete(0,'end')
                    Ei.current(0)
                    R2.select()
                    ent.lift()
                    return
                except:
                    messagebox.showinfo(parent=ent,title="Error",message="Possiblity and existing item code")
                    return
            else:
                messagebox.showinfo(parent=ent,title="Value Required",message="Enter All Value")
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
    #Definition for stock input
    def stockinput(self,w):
        if self.checkfile('msw.db'):
            self.addstock(w)
            return
        else:
            ans=messagebox.askquestion(parent=w,title="No Stock file",message="Press Yes to created new file")
            if ans=='yes':
                con=sqlite3.connect('MSW.db')
                con.execute('''create table stock (Itemcode int primary key not null,Description text not null,HSN int not null,MFG int not null,EXP int not null,GST float not null,Dealer text not null,InvoiceNumber text not null,Price float not null,Units int not null,Utype text not null,Itemtype text not null);''')
                con.commit()
                con.execute('''create table sales (Itemcode int not null,Description text not null,Qty float not null,utype text not null,HSN int not null,Price not null,CGST float not null,SGST float not null,discount float not null,cost float not null,AadharNumber int not null,CustomerDetail text not null,Bill text not null,Date int not null,Return text not null,Itemtype text not null);''')
                con.commit()
                messagebox.showinfo(parent=w,title='Success',message='Stock file created')
                con.close()
                return
            return         
        return
    #Definition for stock view
    def stockview(self,w,itype):
        if self.checkfile('msw.db'):
            con=sqlite3.connect("MSW.db")
            con.execute("DROP TABLE IF EXISTS temp")
            con.commit()
            if itype!='':
                sql="CREATE TABLE IF NOT EXISTS temp AS SELECT Itemcode,Description,HSN,MFG,EXP,GST,Dealer,InvoiceNumber,Price,Units,Utype,Itemtype FROM stock WHERE itemtype is '%s'"%(itype)
                con.execute(sql)
                wdb.view('msw.db','temp',w)
            else:
                wdb.view('msw.db','stock',w)
            con.execute("DROP TABLE IF EXISTS temp")
            con.commit()
            con.close()
            return
        else:
            messagebox.showinfo(parent=w,title='File not found',message=' No stock file!!')
            return
    #Definition for stock update
    def stockupdate(self,w):
        if self.checkfile('msw.db'):
            wdb.update('msw.db','stock',w)
            return
        else:
            messagebox.showinfo(parent=w,title='File not found',message='No stock file !!')
            return


#stock window definiton
def stockwin():
    sw=stockwindow()
    sbox=Toplevel()
    sbox.title("Stock Window")
    sbox.geometry("500x450")
    def block(ins):    
            if ins=='1' or ins=='0':
                return False
            elif ins=='-1':
                return True
    itype=gstrdata.getitemtype()
    B1=Button(sbox,text="Stock I/P",command=lambda x=sbox:sw.stockinput(x))
    B1.pack(side='top',pady=30)
    frametop=Frame(sbox,bd=10)
    frametop.pack(side='top')
    Lit=Label(frametop,text="Item type")
    Lit.pack(side='left')
    Ei=ttk.Combobox(frametop,width=20,values=itype,validate='key')
    Ei.pack(side='left')
    Ei['validatecommand']=(Ei.register(block),'%d')
    B2=Button(sbox,text="View Stock",command=lambda x=sbox:sw.stockview(x,Ei.get()))
    B2.pack(side='top',pady=10)
    B3=Button(sbox,text="Update stock",command=lambda x=sbox:sw.stockupdate(x))
    B3.pack(side='top',pady=10)
    def close():
        sbox.destroy()
        return
    BE=Button(sbox,text="  Exit  ",command=close)
    BE.pack(side='top',pady=15)
    sbox.lift()
    sbox.mainloop()
    return

    
