from tkinter import *
from tkinter import messagebox
import sqlite3
import datetime
import time

def returnwin():
    retbox=Toplevel()
    retbox.title("Return Product")
    frametop=Frame(retbox,bd=10)
    frametop.pack(side='top')
    photo=PhotoImage(file='returnimg.png')
    LT=Label(frametop,image=photo)
    LT.pack(side='top')
    frameget=Frame(retbox,bd=10)
    frameget.pack(side='top')
    Lg=Label(frameget,text="Enter Bill Number")
    Lg.pack(side='left')
    Eg=Entry(frameget,text="bill number entry")
    Eg.pack(side='left')
    def getdet():
        s1=str(Eg.get().upper())
        s=s1.replace(" ","")
        if len(s)==13:
            con=sqlite3.connect("MSW.db")
            cur=con.execute("select bill,return,date from sales")
            lis=''
            cn=0#count of total returned items
            tn=0#total count of items purchased in bill
            billd='0'#bill date to avoid runtime error incase bill does not exist
            tel=cur.fetchall()
            date=datetime.date.today()
            for i in tel:
                if s==i[0]:
                    billd=i[2]
                    tn=tn+1
                    lis=i[0]
                    if i[1]=='Y':
                        cn=cn+1
            if billd=='0':
                messagebox.showinfo(parent=retbox,title="Sorry",message="Bill number not found!!")
                return
            yr=''
            mn=''
            da=''
            ref=0
            for l in billd:
                if ref==0:
                    if l!='-':
                        da=l+da
                    else:
                        ref=1
                elif ref==1:
                    if l!='-':
                        mn=l+mn
                    else:
                        ref=2
                else:
                    if ref==2 and l!='-':
                        yr=l+yr
            def reverse(s):
                rv=''
                for l in s:
                    rv=l+rv
                return rv
            da=int(reverse(da))
            mn=int(reverse(mn))
            yr=int(reverse(yr))
            billd=datetime.date(yr,mn,da)
            mcdate=date-datetime.timedelta(days=7)#last date to return product
            flag=0
            if billd > mcdate:
                flag=1
            con.close()
            if lis!='' and cn!=tn and tn!=0 and flag==1:
                retbox.destroy()
                retbox2=Toplevel()
                retbox2.state("zoomed")
                frametop=Frame(retbox2,bd=10)
                frametop.pack(side='top',fill='x',pady=10)
                Lbn=Label(frametop,text=str("Bill Number :\t"+lis))
                Lbn.pack(side='top')
                frametitle=Frame(retbox2,bd=10)
                frametitle.pack(side='top',fill='x',pady=10)
                Lsn=Label(frametitle,text="S.No")
                Lsn.pack(side='left',ipadx=20)
                Lic=Label(frametitle,text="Item Code")
                Lic.pack(side='left',ipadx=10)
                Ld=Label(frametitle,text="Description")
                Ld.pack(side='left',ipadx=50)
                Lhsn=Label(frametitle,text="\t\t\t\t HSN")
                Lhsn.pack(side='left')
                Lqty=Label(frametitle,text="\tQty")
                Lqty.pack(side='left',ipadx=2)
                Lprice=Label(frametitle,text=" \t    Cost")
                Lprice.pack(side='left')
                Lcgst=Label(frametitle,text="\tCGST")
                Lcgst.pack(side='left')
                Lsgst=Label(frametitle,text="   SGST")
                Lsgst.pack(side='left')
                Ltot=Label(frametitle,text="       Total")
                Ltot.pack(side='left')
                Lcust=Label(frametitle,text="\tCustomer detail")
                Lcust.pack(side='left')
                Lan=Label(frametitle,text="\t\tAadhar number")
                Lan.pack(side='left')
                #Ldis=Label(frametitle,text='Discount')
                #Ldis.pack(side='left')
                canvas=Canvas(retbox2)
                frame2=Frame(canvas,height=300,width=300)
                frame2.pack(side='top')
                hsb=Scrollbar(canvas,orient='horizontal',command=canvas.xview)
                vsb=Scrollbar(canvas,orient='vertical',command=canvas.yview)
                canvas.configure(xscrollcommand=hsb.set,yscrollcommand=vsb.set)
                hsb.pack(side="bottom",fill='x')
                vsb.pack(side="right",fill='y')
                canvas.pack(side="top",fill='both',expand=True)
                canvas.create_window((5,5),window=frame2,anchor="nw")
                def onFrameConfigure(canvas):
                    canvas.configure(scrollregion=canvas.bbox("all"))
                frame2.bind("<Configure>",lambda event,canvas=canvas:onFrameConfigure(canvas))
                frameb2=Frame(retbox2,height=200)
                frameb2.pack(side='top',fill='x',pady=10)
                con=sqlite3.connect('MSW.db')
                det=con.execute("select * from sales where Bill is '%s' and return is 'N'"%(lis))
                labelnum=0
                def block(ins):
                    if ins=='1' or ins=='0':
                        return False
                    elif ins=='-1':
                        return True
                 
                for i in det:
                    #print(i)
                    ic=StringVar(value=i[0])
                    desc=StringVar(value=i[1])
                    hsn=StringVar(value=i[4])
                    qty=StringVar(value=i[2])
                    utype=StringVar(value=i[3])
                    price=StringVar(value=i[5])
                    cgst=StringVar(value=i[6])
                    sgst=StringVar(value=i[7])
                    disc=StringVar(value=i[8])
                    cost=StringVar(value=i[9])
                    custdet=StringVar(value=i[11])
                    aadharnum=StringVar(value=i[10])
                    billno=StringVar(value=i[11])
                    retsts=StringVar(value=i[12])
                    labelnum=labelnum+1
                    frameitem=Frame(frame2,bd=20)
                    frameitem.pack(side='top')
                    L1=Label(frameitem,text=str(labelnum))
                    E2=Entry(frameitem,text='Itemcode',validate='key',textvariable=ic)
                    E2['validatecommand']=(E2.register(block),'%d')
                    E3=Entry(frameitem,text="Description",validate='key',textvariable=desc,width=50)
                    E3['validatecommand']=(E3.register(block),'%d')
                    E4=Entry(frameitem,text="HSN",validate='key',textvariable=hsn,width=10)
                    E4['validatecommand']=(E4.register(block),'%d')
                    E5=Entry(frameitem,text="QTY",validate="key",textvariable=qty,width=8)
                    E5['validatecommand']=(E5.register(block),'%d')
                    E6=Entry(frameitem,text="utype",validate="key",textvariable=utype,width=5)
                    E6['validatecommand']=(E6.register(block),'%d')
                    E7=Entry(frameitem,text='Price per qty',validate="key",textvariable=price,width=10)
                    E7['validatecommand']=(E7.register(block),'%d')
                    E8=Entry(frameitem,text="CGST",validate="key",textvariable=cgst,width=8)
                    E8['validatecommand']=(E8.register(block),'%d')
                    E9=Entry(frameitem,text='SGST',validate="key",textvariable=sgst,width=8)
                    E9['validatecommand']=(E9.register(block),'%d')
                    E10=Entry(frameitem,text='Total',validate='key',textvariable=cost,width=10)
                    E10['validatecommand']=(E10.register(block),'%d')
                    E11=Entry(frameitem,text='Customer Detail',validate='key',textvariable=custdet,width=30)
                    E11['validatecommand']=(E11.register(block),'%d')
                    E12=Entry(frameitem,text="Aadhar number",validate='key',textvariable=aadharnum,width=15)
                    E12['validatecommand']=(E12.register(block),'%d')
                    #E13=Entry(frameitem,text="Discount",validate='key',textvariable=disc,width=15)
                    #E13['validatecommand']=(E13.register(block),'%d')
                    def retitem(ic,qty,cost):
                        #code to return item
                        msg=str("Return succcessful! Please refund Rs."+cost.get())
                        q=str(qty.get())
                        i=str(ic.get())
                        r='Y'
                        con.execute("update stock set units = units + %s where itemcode = %s"%(q,i))
                        con.execute("update sales set return = '%s' where itemcode is '%s' and bill is '%s'"%(r,i,lis))
                        con.commit()
                        messagebox.showinfo(parent=retbox2,title="Success",message=msg)
                        retbox2.destroy()
                        return
                    Retbut=Button(frameitem,text="Return",command=lambda ic=ic,qty=qty,cost=cost:retitem(ic,qty,cost))
                    L1.pack(side='left',padx=5)
                    E2.pack(side='left',padx=5)
                    E3.pack(side='left',padx=5)
                    E4.pack(side='left',padx=5)
                    E5.pack(side='left',padx=5)
                    E6.pack(side='left',padx=5)
                    E7.pack(side='left',padx=5)
                    E8.pack(side='left',padx=5)
                    E9.pack(side='left',padx=5)
                    E10.pack(side='left',padx=5)
                    E11.pack(side='left',padx=5)
                    E12.pack(side='left',padx=5)
                    #E13.pack(side='left',padx=5)
                    Retbut.pack(side='left',padx=5)
                con.close
                def ex():
                    retbox2.destroy()
                    return
                Ex=Button(frameb2,text='Exit',command=ex)
                Ex.pack(side='top',pady=10)
            elif tn!=0:
                if tn==cn and flag==1:
                    messagebox.showinfo(parent=retbox,title="Info",message="No items from this bill to return found or all items have been returned")
                    return
                messagebox.showinfo(parent=retbox,title="Failure",message="Return date exceeded limit")
                return
        else:
            messagebox.showinfo(parent=retbox,title="Error",message="Bill number does not match criteria")
            
        return
    Bg=Button(frameget,text="get details of bill number",command=getdet)
    Bg.pack(side='left')   
    frameb=Frame(retbox,height=20)
    frameb.pack(side='top',fill='x',pady=10)
    def ex():
        retbox.destroy()
        return
    Ex=Button(frameb,text='Exit',command=ex)
    Ex.pack(side='right',padx=200,pady=10)
    retbox.mainloop()

#returnwin()
