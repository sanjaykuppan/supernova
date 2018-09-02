from tkinter import *
import datetime
import sqlite3
import re
from tkinter import messagebox

global l,boxup
l=[]
boxup=0


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
    
    def addproduct(self,frame2,tv):
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
            def block(ins):
                if ins=='1' or ins=='0':
                    return False
                elif ins=='-1':
                    return True
            Lprice=Label(master=self.box,text='Price')
            Ld=Label(master=self.box,text='Description')
            Lqty=Label(self.box,text='Quantity Available')
            Lqtype=Label(self.box,text='Quantity type')
            Lqreq=Label(self.box,text='Quantity Required')
            Lcgst=Label(self.box,text='CGST')
            Lsgst=Label(self.box,text='SGST')
            Lat=Label(self.box,text='@')
            Lval=Label(self.box,text='Cost')
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
            ic=IntVar()
            ilist=[]
            def fetch():
                t=eic.get()
                con=sqlite3.connect('MSW.db')
                try:
                    stkd=con.execute("select description,hsn,gst,price,units,utype from stock where itemcode is %s"%(t))
                    ic.set(eic.get())
                    d=stkd.fetchall()
                    desc.set(d[0][0])
                    hsn.set(d[0][1])
                    gst.set(d[0][2])
                    price.set(d[0][3])
                    gstv.set(round((gst.get()/100)*price.get(),2))
                    q.set(d[0][4])
                    qt.set(d[0][5])
                except:
                    messagebox.showinfo(parent=self.box,title='Error',message="Wrong input")
                con.close()
                return
            def val(inpt,ins):
                try:                    
                    if ins=='1' :
                        inpt=int(inpt) if qt.get()=='PCS' else float(inpt)
                        if inpt!=0:
                            cval.set(round(inpt*((2*gstv.get())+(price.get())),2))
                            return True
                        return False
                    if ins == '0' and not len(str(inpt)) >0:
                        cval.set(0)
                        return True
                    elif ins== '0' and len(str(inpt))>0:
                        inpt=int(inpt) if qt.get()=='PCS' else float(inpt)
                        cval.set(round(inpt*(2*gstv.get()+(price.get())),2))
                        return True
                    return False
                except:
                    print ('except')
                    return False
            Eqreq=Entry(self.box,text='Quantity Required',validate="key")
            Eqreq['validatecommand']=(Eqreq.register(val),'%P','%d')
            Eqreq.grid(row=10,column=4)
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
                            tv.set(round((tv.get()-cval.get()),2))
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
                        l.append(ilist)
                        self.box.destroy()
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
    def billproduct(self,bbox,ecd,ean,date,bnt,cv):
        global l
        aadharnumber=ean.get()
        customerdet=ecd.get()
        bill=bnt
        ret='N'
        if len(str(ean.get()))<12:
            messagebox.showinfo(parent=bbox,title="Error",message="Aadhar is 12 digit! please enter valid aadhar number")
            return
        if len(str(ecd.get()))<1:
            messagebox.showinfo(parent=bbox,title="Error",message="Enter Customer Detail")
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
                total=str(v[9].get())
                con=sqlite3.connect('MSW.db')
                con.execute('''insert into sales (itemcode,description,qty,utype,hsn,price,cgst,sgst,cost,AadharNumber,CustomerDetail,bill,date,return) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?);''',(itemcode,description,qty,utype,hsn,price,cgst,sgst,total,aadharnumber,customerdet,bill,date,ret))
                qaval=con.execute("select units from stock where itemcode is %s"%(itemcode))
                a=(str(qaval.fetchone()[0]))
                qupd=int(a)-int(qty)
                con.execute(" update stock set units = %s where itemcode = %s"%(qupd,itemcode))
                con.commit()
                con.close()
            messagebox.showinfo(parent=bbox,title="Success",message="Bill successful")
            bbox.destroy()
                #code pending for printer output
            return
        elif l==[]:
            messagebox.showinfo(parent=bbox,title="Error",message="No item to Bill please add item!!")
            return
        
        return
    

def MainWindow():
    global l
    l=[]
    bw=billwindow()
    bbox=Toplevel()
    bbox.title("Billing")
    bbox.state('zoomed')
    photo=PhotoImage(file='BW.png')
    frametop=Frame(bbox,bd=10)
    frametop.pack(side='top')
    LT=Label(frametop,image=photo)
    LT.pack(side='top')
    frame1=Frame(bbox)
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
    Ecd['validatecommand']=(Ecd.register(Val),'%d',41,'%P')
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
    frametitle=Frame(bbox)
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
    canvas=Canvas(bbox)
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
    tv=DoubleVar()#amount to be paid in total
    frameb=Frame(bbox,height=200)
    frameb.pack(side='top',fill='x')
    add=Button(frameb,text='Add Item',command=lambda w=frame2,tv=tv:bw.addproduct(w,tv))
    add.grid(row=0,column=5,padx=500)
    billphoto=PhotoImage(file='bill.png')
    billitem=Button(frameb,image=billphoto,command=lambda w=bbox,ecd=Ecd,ean=Ean,date=date,bnt=bnt,tv=tv:bw.billproduct(w,ecd,ean,date,bnt,tv))
    billitem.grid(row=1,column=1,padx=50)
    Lc=Label(frameb,text='Payable Amount\tRs.')
    Lc.grid(row=1,column=2)
    Ec=Entry(frameb,text='Payable amount',textvariable=tv,validate='key',width=10)
    Ec['validatecommand']=(Ec.register(block),'%d')
    Ec.grid(row=1,column=3)
    def ex():
        bbox.destroy()
        return
    framex=Frame(bbox)
    framex.pack(side='bottom',fill='x')
    Ex=Button(framex,text='Exit',command=ex)
    Ex.pack(side='right',padx=200,pady=10)
    bbox.mainloop()
    
#MainWindow()
