from tkinter import *
import datetime
import sqlite3
import re
from tkinter import messagebox
import win32ui
import win32print
import time
import win32com.client
import json
import os.path
import getstoredata as gstrdata

global l,boxup,billup,printerflag
l=[]
boxup=0
billup=False
printerflag=False

class AutocompleteEntry(Entry):
    def __init__(self, lista,box, *args, **kwargs):
        
        Entry.__init__(self,master=box, *args, **kwargs)
        self.lista = lista
        self.box=box
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()
        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.lb_up = False
        return
    def changed(self, name, index, mode):  
        if self.var.get() == '' and self.lb_up == True:
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = Listbox(master=self.box)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        return
    def selection(self, event):
        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)
        return
    def up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index)
        return
    def down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index)
        return
    def comparison(self): 
        pattern = re.compile('.*' + self.var.get() + '.*')
        l=[]
        for i in self.lista:
            i=str(i)
            l.append(i)
        return [w for w in l if re.match(pattern, w)]


class billwindow:
    
    def addproduct(self,frame2,tv,twd,td,Ediscount,Adbut,Rdbut,disaflag,disrflag):
        global boxup
        try:
            a=self.box.winfo_exists()
            messagebox.showinfo(parent=self.box,title="Error",message="Window already up")
            self.box.lift()
        except:
            boxup=0
        if boxup==0:
            self.box=Toplevel(master=frame2)
            boxup=1
            self.box.title("Add Product to bill")
            self.box.geometry("900x600")
            lic=Label(self.box,text="Item Code")
            lic.grid(row=0,column=0)
            con=sqlite3.connect('MSW.db')
            cur=con.execute("select ITEMCODE from stock")
            ic=[]
            tel=cur.fetchall()
            for i in tel:
                ic.append(i[0])
            con.close()
            eic=AutocompleteEntry(ic,self.box)
            eic.grid(row=0,column=1)
            desc=StringVar()
            price=DoubleVar()
            q=DoubleVar()
            qt=StringVar()
            hsn=StringVar()
            gst=DoubleVar()
            gstv=DoubleVar()
            cval=DoubleVar()
            itype=StringVar()
            def block(ins):
                if ins=='1' or ins=='0':
                    return False
                elif ins=='-1':
                    return True
            Lprice=Label(master=self.box,text='Price')
            Litype=Label(master=self.box,text='Item Type')
            Ld=Label(master=self.box,text='Description')
            Lqty=Label(self.box,text='Quantity Available')
            Lqtype=Label(self.box,text='Quantity type')
            Lqreq=Label(self.box,text='Quantity Required')
            Lcgst=Label(self.box,text='CGST')
            Lsgst=Label(self.box,text='SGST')
            Lat=Label(self.box,text='@')
            Lval=Label(self.box,text='Cost')
            Eitype=Entry(self.box,text='Item type',textvariable=itype,validate='key')
            Eitype['validatecommand']=(Eitype.register(block),'%d')
            Ed=Entry(self.box,text='description',textvariable=desc,validate='key')
            Ed['validatecommand']=(Ed.register(block),'%d')
            Eprice=Entry(self.box,text='Price',textvariable=price,validate='key')
            Eprice['validatecommand']=(Eprice.register(block),'%d')
            Eqty=Entry(self.box,text='Quantity available',textvariable=q,validate='key')
            Eqty['validatecommand']=(Eqty.register(block),'%d')
            Eqtype=Entry(self.box,text='Quantity Type',textvariable=qt,validate='key')
            Eqtype['validatecommand']=(Eqtype.register(block),'%d')
            Ecgst=Entry(self.box,text='CGST',textvariable=gstv,validate='key')
            Ecgst['validatecommand']=(Ecgst.register(block),'%d')
            Eat=Entry(self.box,text='gst rate',textvariable=gst,validate='key')
            Eat['validatecommand']=(Eat.register(block),'%d')
            Esgst=Entry(self.box,text='SGST',textvariable=gstv,validate='key')
            Esgst['validatecommand']=(Esgst.register(block),'%d')
            Eval=Entry(self.box,text='Quantity cost',textvariable=cval,validate='key')
            Eval['validatecommand']=(Eval.register(block),'%d')
            Litype.grid(row=1,column=3,ipadx=6)
            Eitype.grid(row=1,column=4)
            Ld.grid(row=2,column=3,ipadx=6)
            Ed.grid(row=2,column=4)
            Lprice.grid(row=3,column=3)
            Eprice.grid(row=3,column=4)
            Lqty.grid(row=4,column=3)
            Eqty.grid(row=4,column=4)
            Lqtype.grid(row=5,column=3)
            Eqtype.grid(row=5,column=4)
            Lcgst.grid(row=6,column=3)
            Ecgst.grid(row=6,column=4)
            Lsgst.grid(row=7,column=3)
            Esgst.grid(row=7,column=4)
            Lat.grid(row=6,column=5)
            Eat.grid(row=6,column=6)
            Lqreq.grid(row=10,column=3,ipady=20)
            Lval.grid(row=10,column=7)
            Eval.grid(row=10,column=8)
            ic=IntVar() #item code text variable
            
            ilist=[]
            def fetch():
                t=eic.get()
                con=sqlite3.connect('MSW.db')
                try:
                    stkd=con.execute("select description,hsn,gst,price,units,utype,itemtype from stock where itemcode is %s"%(t))
                    ic.set(eic.get())
                    d=stkd.fetchall()
                    desc.set(d[0][0])
                    hsn.set(d[0][1])
                    gst.set(d[0][2])
                    price.set(d[0][3])
                    gstv.set(round((gst.get()/200)*price.get(),2))  #get gst value for one piece(CGST or SGST)
                    q.set(d[0][4])
                    qt.set(d[0][5])
                    itype.set(d[0][6])
                except:
                    messagebox.showinfo(parent=self.box,title='Error',message="Wrong input")
                con.close()
                return
            def val(inpt,ins):
                try:                    
                    if ins=='1' :
                        inpt=int(inpt) if qt.get()=='PCS' else float(inpt)
                        if inpt!=0:
                            cval.set(round(inpt*((2*gstv.get())+(price.get())),2)) #total value in add window
                            return True
                        return False
                    if ins == '0' and not len(str(inpt)) >0:
                        cval.set(0)                                       #set total value in add window to zero if qty is none 
                        return True
                    elif ins== '0' and len(str(inpt))>0:
                        inpt=int(inpt) if qt.get()=='PCS' else float(inpt)
                        cval.set(round(inpt*((2*gstv.get())+(price.get())),2)) #total value in add window 
                        return True
                    return False
                except:
                    print ('except')
                    return False
            Eqreq=Entry(self.box,text='Quantity Required',validate="key")
            Eqreq['validatecommand']=(Eqreq.register(val),'%P','%d')
            Eqreq.grid(row=10,column=4)
            Eqreq.delete(0,'end')
            Eqreq.delete(first=0,last=None)
            fetchb=Button(self.box,text='Fetch details',command=fetch)
            fetchb.grid(row=0,column=2,ipadx=2,ipady=5)
            def addcheck():
                try:
                    global l
                    if l!=[]:
                        for temp in l:
                            existcode=temp[1].get()
                            if existcode==str(ic.get()):
                                messagebox.showinfo(parent=self.box,title="Error",message="Item code already added")
                                return              
                    if int(Eqreq.get()) <= int(q.get()) :
                        frameitem=Frame(frame2,bd=20)
                        frameitem.pack(side='top')
                        sno=StringVar()
                        eqreq=StringVar()
                        eqreq.set(Eqreq.get())
                        L1=Label(frameitem,text=sno.get())
                        if l==[]:
                            L1.config(text='1')
                        else:
                            temp=l[-1]
                            L1.config(text=str(int(temp[0].cget("text"))+1))
                        E2=Entry(frameitem,text='Itemcode',validate='key',textvariable=ic)
                        E2['validatecommand']=(E2.register(block),'%d')
                        E3=Entry(frameitem,text="Description",validate='key',textvariable=desc,width=50)
                        E3['validatecommand']=(E3.register(block),'%d')
                        E4=Entry(frameitem,text="HSN",validate='key',textvariable=hsn,width=10)
                        E4['validatecommand']=(E4.register(block),'%d')
                        E5=Entry(frameitem,text="QTY",validate="key",textvariable=eqreq,width=8)
                        E5['validatecommand']=(E5.register(block),'%d')
                        E6=Entry(frameitem,text="utype",validate="key",textvariable=qt,width=5)
                        E6['validatecommand']=(E6.register(block),'%d')
                        E7=Entry(frameitem,text='Price per qty',validate="key",textvariable=price,width=10)
                        E7['validatecommand']=(E7.register(block),'%d')
                        E8=Entry(frameitem,text="CGST",validate="key",textvariable=gstv,width=5)
                        E8['validatecommand']=(E8.register(block),'%d')
                        E9=Entry(frameitem,text='SGST',validate="key",textvariable=gstv,width=5)
                        E9['validatecommand']=(E9.register(block),'%d')
                        E10=Entry(frameitem,text='Total',validate='key',textvariable=cval,width=10)
                        E10['validatecommand']=(E10.register(block),'%d')
                        def delitem():
                            global l
                            i=int(L1.cget("text"))-1
                            frameitem.destroy()
                            del l[i]
                            sno=1
                            for v in l:
                                    v[0].config(text=sno)
                                    sno=sno+1
                            tv.set(round((tv.get()-cval.get()),1))
                            Ediscount.config(state="normal")
                            td.set(0)
                            twd.set(round(tv.get()))
                            Adbut.config(state="active")
                            Rdbut.config(state="disabled")
                            disaflag.set("active")
                            disrflag.set("disabled")
                            return
                        Delb=Button(frameitem,text="Delete",command=delitem)
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
                        Delb.pack(side='left',padx=5)
                        tv.set(round((tv.get()+cval.get()),2))
                        twd.set(round(tv.get()))
                        ilist.append(L1)
                        ilist.append(E2)
                        ilist.append(E3)
                        ilist.append(E4)
                        ilist.append(E5)
                        ilist.append(E6)
                        ilist.append(E7)
                        ilist.append(E8)
                        ilist.append(E9)
                        ilist.append(E10)
                        ilist.append(itype.get())
                        l.append(ilist)
                        self.box.destroy()
                        Ediscount.config(state="normal")
                        td.set(0)
                        itype.set('')
                        Adbut.config(state="active")
                        Rdbut.config(state="disabled")
                        disaflag.set("active")
                        disrflag.set("disabled")
                        return
                    else:
                        messagebox.showinfo(parent=self.box,title='Error',message='Quantity not available !! check entry')
                        return
                except:
                    messagebox.showinfo(parent=self.box,title='Error',message='Add item Failure')
            addb=Button(self.box,text="Add",command=addcheck)
            addb.grid(row=12,column=5)
        else:
            try:
                self.box.lift()
            except:
                boxup=0
        return
    #command to bill product
    def billproduct(self,bbox,ecd,ean,date,bnt,cv,edis,twd):
        global l,printerflag
        #printerflag=True  #set this to true to get printer output by default and for testing without printer
        aadharnumber=ean.get()
        customerdet=ecd.get()
        bill=bnt
        ret='N'
        curdate=datetime.date.today().strftime("%d-%m-%Y")
        curtime=datetime.datetime.now().time().strftime('%I:%M %p')
        #if len(str(ean.get()))<12:
        #    messagebox.showinfo(parent=bbox,title="Error",message="Aadhar is 12 digit! please enter valid aadhar number")
        #    return
        if len(str(ecd.get()))<1:
            messagebox.showinfo(parent=bbox,title="Error",message="Enter Customer Detail")
            return
        if edis.get()>str(cv):
            messagebox.showinfo(parent=bbox,title="Error",message="Discount is greater than total cost")
            return
        if l!=[]:
            for v in l:
                itemcode=str(v[1].get())
                description=str(v[2].get())
                hsn=str(v[3].get())
                qty=str(v[4].get())
                utype=str(v[5].get())
                price=str(v[6].get())
                sgst=str(v[7].get())
                cgst=str(v[8].get())
                discount=str(edis.get())
                total=str(v[9].get())
                itemtype=str(v[10])
                con=sqlite3.connect('MSW.db')
                con.execute('''insert into sales (itemcode,description,qty,utype,hsn,price,cgst,sgst,discount,cost,AadharNumber,CustomerDetail,bill,date,return,Itemtype) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);''',(itemcode,description,qty,utype,hsn,price,cgst,sgst,discount,total,aadharnumber,customerdet,bill,date,ret,itemtype))
                qaval=con.execute("select units from stock where itemcode is %s"%(itemcode))
                a=(str(qaval.fetchone()[0]))
                qupd=int(a)-int(qty)
                con.execute(" update stock set units = %s where itemcode = %s"%(qupd,itemcode))
                con.commit()
                con.close()
            #code for printer output create a storedetail.json file to feed store details
            if printerflag:
                if os.path.isfile("storedetail.json"):
                    strname=gstrdata.getdata("store")
                    phno=gstrdata.getdata("number")
                    gst=gstrdata.getdata("gst")
                    branch=gstrdata.getdata("branch")
                    seed=gstrdata.getdata("Seed")
                    pesticide=gstrdata.getdata("Pesticide")
                    fertilizer=gstrdata.getdata("Fertilizer")
                    tinno=gstrdata.gettinno()
                else:
                    strname="Agro center"
                    phno=""
                    gst=""
                    branch=""
                    seed=""
                    pesticide=""
                    fertilizer=""
                    tinno=""
                
                x=0;y=0  #mark x and y for co-ordinates for printing
                #try:
                hDC=win32ui.CreateDC()
                hDC.CreatePrinterDC()
                hDC.StartDoc("Bill")
                hDC.StartPage()
                font=win32ui.CreateFont({'name':'Times New Roman','height':40,'weight':40})
                font1=win32ui.CreateFont({'name':'Arial','height':25,'weight':20})
                font2=win32ui.CreateFont({'name':'Arial','height':30,'weight':40})
                hDC.SelectObject(font)
                x=10
                hDC.TextOut(x,y,strname)
                hDC.SelectObject(font1)
                y+=40;x=0
                hDC.TextOut(x,y,("Branch:"+branch+" Date:"+curdate+" "+curtime))
                y+=30;x=0
                hDC.TextOut(x,y,"GST:"+gst)
                y+=30;x=0
                hDC.TextOut(x,y,"S.L. NO:"+seed)
                y+=30;x=0
                hDC.TextOut(x,y,"P.L. NO:"+pesticide)
                y+=30;x=0
                hDC.TextOut(x,y,"F.L. NO:"+fertilizer)
                y+=30;x=0
                hDC.TextOut(x,y,"TIN.No:"+tinno)
                y+=30;x=0
                hDC.TextOut(x,y,"Ph.no:"+phno)
                y+=30;x=0
                hDC.TextOut(x,y,"Aadhar number:"+aadharnumber)
                y+=30
                hDC.TextOut(x,y,customerdet)
                y+=30
                hDC.TextOut(x,y,"Bill No."+bill)
                x=0;y+=30
                hDC.TextOut(x,y,"code  Item")
                x=350;hDC.TextOut(x,y,"Qty")
                #x=30;y+=30;hDC.TextOut(x,y,"Price")
                #x+=80;hDC.TextOut(x,y,"CGST")
                #x+=80;hDC.TextOut(x,y,"SGST")
                x+=80;hDC.TextOut(x,y,"cost")
                #sno=1#count
                gtot=0;gsttot=0;tot=0
                for v in l:
                    y+=30;x=0
                    hDC.TextOut(x,y,str(v[1].get())+"  "+str(v[2].get()))
                    x=340
                    hDC.TextOut(x,y,str(v[4].get()))#QTY
                    #x=30;y+=30;hDC.TextOut(x,y,str(v[6].get()))#price of one qty
                    #x+=80;hDC.TextOut(x,y,str(float(v[7].get())))#CGST
                    #x+=80;hDC.TextOut(x,y,str(float(v[7].get())))#SGST
                    gsttot+=float(v[7].get())*float(v[4].get()) #CGST or SGST Total
                    x+=80
                    hDC.TextOut(x,y,str(float(v[9].get())))#cost
                    #sno+=1;
                    gtot+=float(v[9].get()) #cost+gst
                    tot+=float(v[6].get())*float(v[4].get())
                    time.sleep(0.25)
                x=0;y+=40
                hDC.TextOut(x,y,"Taxable Amount")
                x+=280;hDC.TextOut(x,y,str(round(tot,2)))
                x=0;y+=40
                hDC.TextOut(x,y,"CGST")
                x+=280;hDC.TextOut(x,y,str(round(gsttot,2)))
                y+=40;x=0;hDC.TextOut(x,y,"SGST")
                x+=280;hDC.TextOut(x,y,str(round(gsttot,2)))
                x=0;y+=40;hDC.TextOut(x,y,"Discount")
                x+=280;hDC.TextOut(x,y,str(round(float(discount),2)))
                x=0;y+=40;hDC.TextOut(x,y,"Total Amount Payable")
                x+=350;hDC.TextOut(x,y,str(round(gtot-float(discount))))
                y+=60;x=120;hDC.TextOut(x,y,"Thank You!")
                #finally:
                hDC.EndPage()
                hDC.EndDoc()
            messagebox.showinfo(parent=bbox,title="Success",message="Bill successful")
            bbox.destroy()
            global billup
            billup=False
            return
        elif l==[]:
            messagebox.showinfo(parent=bbox,title="Error",message="No item to Bill please add item!!")
            return
        
        return
    

def MainWindow():
    global billup,l,printerflag
    wmi=win32com.client.GetObject("winmgmts:")
    dl=[]
    printerflag=False
    for usb in wmi.InstancesOf("Win32_USBHub"):
        dl.append(usb.DeviceID)
    for d in dl:
        if d.find("VID_0456&PID_0808") != -1:#check printer online
            printerflag=True
    goinside=False
    if printerflag:
        goinside=True
    else:
        goinside=messagebox.askyesno(title="Printer offline",message="Printer is offline do you want to continue?")
    if (goinside):
        billup=True
        l=[]
        bw=billwindow()
        MainWindow.bbox=Toplevel()
        MainWindow.bbox.title("Billing")
        MainWindow.bbox.state('zoomed')
        photo=PhotoImage(file='BW.png')
        frametop=Frame(MainWindow.bbox,bd=10)
        frametop.pack(side='top')
        LT=Label(frametop,image=photo)
        LT.pack(side='top')
        frame1=Frame(MainWindow.bbox)
        frame1.pack(side='top')
        def Val(ins,maxlen,value):#parameters(is input made,max lenght)    
            maxlen=int(maxlen)
            if ins =='1' :#check insert true
                if not len(value)<maxlen:
                    return False 
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
        def block(ins):    
            if ins=='1' or ins=='0':
                return False
            elif ins=='-1':
                return True
        Lcd=Label(frame1,text="Enter Customer Detail")
        Lcd.grid(row=1,column=0,sticky='E')
        Ecd=Entry(frame1,text="Customer Detail",bd=10,validate='key',width=40)
        Ecd['validatecommand']=(Ecd.register(Val),'%d',38,'%P')
        Ecd.grid(row=1,column=1)
        Ecd.delete(0,'end')
        Lan=Label(frame1,text="\tEnter Aadhaar Number")
        Lan.grid(row=1,column=2)
        Ean=Entry(frame1,text="Aadhar Number",bd=10,validate='key',width=13)
        Ean['validatecommand']=(Ean.register(intval),'%d',13,'%P')
        Ean.grid(row=1,column=3)
        Ean.delete(0,'end')
        Ldr=Label(frame1,text="\tDate :")
        Ldr.grid(row=1,column=4)
        date=datetime.date.today().strftime("%d-%m-%Y")
        Ld=Label(frame1,text=date)
        Ld.grid(row=1,column=5)
        Lb=Label(frame1,text="\tBill Number :")
        Lb.grid(row=1,column=6)
        dv=datetime.date.today().strftime("%d%m")
        tiv=datetime.datetime.now().time().strftime("%H%M%S")
        bnt="SKA"+dv+tiv
        Lbn=Label(frame1,text=bnt)#bill number
        Lbn.grid(row=1,column=7)
        frametitle=Frame(MainWindow.bbox)
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
        Ltot=Label(frametitle,text="     Total")
        Ltot.pack(side='left')
        frametitle.pack(side='top',fill='x',pady=10)
        canvas=Canvas(MainWindow.bbox)
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
        def disapply(disaflag,disrflag,td,twd,adb,rdb,edis):
            if(disaflag.get()=="active" and td.get()!=0 and twd.get()>td.get()):
                disaflag.set("disabled")
                disrflag.set("active")
                adb.config(state=disaflag.get())
                rdb.config(state=disrflag.get())
                twd.set(round(twd.get()-td.get()))
                edis.config(state='disabled')
        def disremove(disaflag,disrflag,td,twd,adb,rdb,edis):
            if(disrflag.get()=="active" and td.get()!=0 ):
                disrflag.set("disabled")
                disaflag.set("active")
                rdb.config(state=disrflag.get())
                adb.config(state=disaflag.get())
                twd.set(round(twd.get()+td.get()))
                td.set(0)
                edis.config(state='normal')
        frame2.bind("<Configure>",lambda event,canvas=canvas:onFrameConfigure(canvas))
        tv=DoubleVar()#amount to be paid without discount
        td=DoubleVar(0)#discount amount in total
        twd=DoubleVar()
        disaflag=StringVar()
        disrflag=StringVar()
        disaflag.set("active")
        disrflag.set("disabled")
        frameb=Frame(MainWindow.bbox,height=200)
        frameb.pack(side='top',fill='x')
        Ediscount=Entry(frameb,text='Discount',textvariable=td,validate='key',width=10)
        Ediscount['validatecommand']=(Ediscount.register(intval),'%d',5,'%P')
        add=Button(frameb,text='Add Item',command=lambda td=td,twd=twd,w=frame2,tv=tv:bw.addproduct(w,tv,twd,td,Ediscount,Adbut,Rdbut,disaflag,disrflag))
        add.grid(row=0,column=8,padx=500)
        Ldiscount=Label(frameb,text='Discount\tRs.')
        Ldiscount.grid(row=0,column=2)
        Ediscount.grid(row=0,column=3)
        Lwdiscount=Label(frameb,text='Total Amount Without discount\tRs.')
        Lwdiscount.grid(row=0,column=6)
        Etotal=Entry(frameb,text="total without discount",textvariable=tv,validate='key',width=10)
        Etotal['validatecommand']=(Etotal.register(block),'%d')
        Etotal.grid(row=0,column=7)
        Adbut=Button(frameb,text="Apply",state=disaflag.get(),command=lambda disaflag=disaflag,disrflag=disrflag,td=td,twd=twd:disapply(disaflag,disrflag,td,twd,Adbut,Rdbut,Ediscount))
        Adbut.grid(row=0,column=4)
        Rdbut=Button(frameb,text="Remove",state=disrflag.get(),command=lambda disaflag=disaflag,disrflag=disrflag,td=td,twd=twd:disremove(disaflag,disrflag,td,twd,Adbut,Rdbut,Ediscount))
        Rdbut.grid(row=0,column=5)
        billphoto=PhotoImage(file='bill.png')
        billitem=Button(frameb,image=billphoto,command=lambda twd=twd,edis=Ediscount,w=MainWindow.bbox,ecd=Ecd,ean=Ean,date=date,bnt=bnt,tv=tv:bw.billproduct(w,ecd,ean,date,bnt,tv,edis,twd))
        billitem.grid(row=1,column=1,padx=50)
        Lc=Label(frameb,text='Payable Amount\tRs.')
        Lc.grid(row=1,column=2)
        Ec=Entry(frameb,text='Payable amount',textvariable=twd,validate='key',width=10)
        Ec['validatecommand']=(Ec.register(block),'%d')
        Ec.grid(row=1,column=3)
        def ex():
            MainWindow.bbox.destroy()
            global billup
            billup=False
            return
        framex=Frame(MainWindow.bbox)
        framex.pack(side='bottom',fill='x')
        Ex=Button(framex,text='Exit',command=ex)
        Ex.pack(side='right',padx=200,pady=10)
        def on_close():
            global billup
            billup=False
            MainWindow.bbox.destroy()
        MainWindow.bbox.protocol("WM_DELETE_WINDOW",on_close)
        MainWindow.bbox.mainloop()

def wincheck():
    global billup
    return billup
    
#MainWindow()
