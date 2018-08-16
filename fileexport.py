#for stock and file export 

import sqlite3
import pandas as pd
import os.path
from tkinter import *
from tkinter import messagebox
import datetime

def exportfile():
    exbox=Toplevel()
    exbox.title("Export window")
    photo=PhotoImage(file='exportwindow.png')
    LT=Label(exbox,image=photo)
    LT.pack(side='top',pady=20)
    def stock(): # for stock export to Excel
        tod=str(datetime.date.today().strftime("%d%m"))
        b=str(datetime.datetime.now().time().strftime("%H%M"))
        fname="stockfile-"+tod+"-"+b+".xlsx"
        con=sqlite3.connect("MSW.db")
        df=pd.read_sql_query("SELECT * from stock",con)
        writer=pd.ExcelWriter(fname)
        df.to_excel(writer,'sheet1','B1',index=False)
        writer.save()
        con.close()
        mes=fname+" has been created successfully!!"
        messagebox.showinfo(parent=exbox,title="Success",message=mes)
        return
    def sale(): # for sales export to Excel
        if os.path.isfile("salefile.xlsx"):
            os.remove("salefile.xlsx")
        top=Toplevel()
        top.geometry("500x500")
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
        Ld=Label(top,text="DD")
        Ld.grid(row=0,column=2)
        Lm=Label(top,text="MM")
        Lm.grid(row=0,column=3)
        Ly=Label(top,text='YYYY')
        Ly.grid(row=0,column=4)
        Lf=Label(top,text="Start Date")
        Lf.grid(row=1,column=1)
        Esd=Entry(top,text="start date dd",bd=2,validate="key",width=2)
        Esd.grid(row=1,column=2)
        Esd["validatecommand"]=(Esd.register(intval),'%d',3,'%P')
        Esm=Entry(top,text="start date mm",bd=2,validate="key",width=2)
        Esm.grid(row=1,column=3)
        Esm["validatecommand"]=(Esm.register(intval),'%d',3,'%P')
        Esy=Entry(top,text="start date yyyy",bd=2,validate="key",width=4)
        Esy.grid(row=1,column=4)
        Esy["validatecommand"]=(Esy.register(intval),'%d',5,'%P')
        Le=Label(top,text="End Date")
        Le.grid(row=2,column=1)
        Eed=Entry(top,text="End date dd",bd=2,validate="key",width=2)
        Eed.grid(row=2,column=2)
        Eed["validatecommand"]=(Eed.register(intval),'%d',3,'%P')
        Eem=Entry(top,text="End date mm",bd=2,validate="key",width=2)
        Eem.grid(row=2,column=3)
        Eem["validatecommand"]=(Eem.register(intval),'%d',3,'%P')
        Eey=Entry(top,text="End date yyyy",bd=2,validate="key",width=4)
        Eey.grid(row=2,column=4)
        Eey["validatecommand"]=(Eey.register(intval),'%d',5,'%P')
        def sub():
            a=Esd.get() and Esm.get() and Esy.get() and Eed.get() and Eem.get() and Eey.get()
            if a:
                sd=int(Esd.get())
                sm=int(Esm.get())
                sy=int(Esy.get())
                ed=int(Eed.get())
                em=int(Eem.get())
                ey=int(Eey.get())
                try:
                    stdate=datetime.date(sy,sm,sd)#start date
                    endate=datetime.date(ey,em,ed)#end date
                    if stdate>datetime.date.today() or endate>datetime.date.today() or stdate>endate:
                        print (1/0)
                    con=sqlite3.connect("MSW.db")
                    cur=con.execute("select bill,date from sales")
                    tel=cur.fetchall()
                    lis=[]
                    def reverse(s):
                        rv=''
                        for l in s:
                            rv=l+rv
                        return rv
                    for i in tel:
                        ref=0
                        yr=''
                        mn=''
                        da=''
                        item=i[1]
                        billn=i[0]
                        for j in item:
                            if ref==0:
                                if j!='-':
                                    da=j+da
                                else:
                                    ref=1
                            elif ref==1:
                                if j!='-':
                                    mn=j+mn
                                else:
                                    ref=2
                            else:
                                if ref==2 and j!='-':
                                    yr=j+yr
                        da=int(reverse(da))
                        mn=int(reverse(mn))
                        yr=int(reverse(yr))
                        dat=datetime.date(yr,mn,da)
                        if stdate<=dat<=endate and billn not in lis:
                            lis.append(billn)
                    std=str(stdate.strftime("%d%m"))
                    endte=str(endate.strftime("%d%m"))
                    entime=str(datetime.datetime.now().time().strftime("%H%M"))
                    fname="salesfile "+std+"-"+endte+"-"+entime+".xlsx"
                    con.execute("DROP TABLE IF EXISTS temp")
                    con.commit()
                    sql="CREATE TABLE IF NOT EXISTS temp AS SELECT Itemcode,Description,Qty,utype,HSN,Price,CGST,SGST,cost,AadharNumber,CustomerDetail,Bill,Date,Return FROM sales WHERE bill IN ({seq})".format(seq=','.join(['?']*len(lis)))
                    con.execute(sql,lis)
                    df=pd.read_sql_query("SELECT * from temp",con)
                    writer=pd.ExcelWriter(fname)
                    df.to_excel(writer,'sheet1','B1',index=False)
                    writer.save()
                    mes=fname+"has been successfully created!!!"
                    messagebox.showinfo(parent=top,title="Success",message=mes)
                    con.execute("DROP TABLE IF EXISTS temp")
                    con.commit()
                    con.close()
                    Esd.delete(0,'end')
                    Esm.delete(0,'end')
                    Esy.delete(0,'end')
                    Eed.delete(0,'end')
                    Eem.delete(0,'end')
                    Eey.delete(0,'end')
                    top.destroy()
                except:
                    messagebox.showinfo(parent=top,title="Error",message="Wrong date!!!")
                    top.lift()
            else:
                messagebox.showinfo(parent=top,title="Error",message="Enter all values")
                top.lift()
                    
            return
        But=Button(top,text="Submit",command=sub)
        But.grid(row=3,column=5,padx=10,pady=10)
        
    Bst=Button(exbox,text="Export Stock Data",command=stock)
    Bst.pack(side='top',pady=10)
    Bsa=Button(exbox,text="Export Sales Data",command=sale)
    Bsa.pack(side='top',pady=10)
    def ex():
        exbox.destroy()
        return
    exbut=Button(exbox,text="Exit",command=ex)
    exbut.pack(side='top',pady=50)
    
    exbox.mainloop()

#exportfile()
