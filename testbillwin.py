from tkinter import *
import datetime
import sqlite3
import re
from tkinter import messagebox


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
    
    def addproduct(self,w,rn,cn):
        box=Toplevel(master=w)
        box.title("Add Product to bill")
        box.geometry("900x600")
        lic=Label(box,text="Item Code")
        lic.grid(row=0,column=0)
        con=sqlite3.connect('MSW.db')
        cur=con.execute("select ITEMCODE from stock")
        ic=[]
        tel=cur.fetchall()
        for i in tel:
            ic.append(i[0])
        con.close()
        eic=AutocompleteEntry(ic,box)
        eic.grid(row=0,column=1)
        desc=StringVar()
        price=DoubleVar()
        q=DoubleVar()
        qt=StringVar()
        hsn=StringVar()
        gst=DoubleVar()
        gstv=DoubleVar()
        cval=DoubleVar()
        Lprice=Label(master=box,text='Price')
        Ld=Label(master=box,text='Description')
        Lqty=Label(box,text='Quantity Available')
        Lqtype=Label(box,text='Quantity type')
        Lqreq=Label(box,text='Quantity Required')
        Lcgst=Label(box,text='CGST')
        Lsgst=Label(box,text='SGST')
        Lat=Label(box,text='@')
        Lval=Label(box,text='Cost')
        Ed=Entry(box,text='description',textvariable=desc)
        Eprice=Entry(box,text='Price',textvariable=price)
        Eqty=Entry(box,text='Quantity available',textvariable=q)
        Eqtype=Entry(box,text='Quantity Type',textvariable=qt)
        Ecgst=Entry(box,text='CGST',textvariable=gstv)
        Eat=Entry(box,text='gst rate',textvariable=gst)
        Esgst=Entry(box,text='SGST',textvariable=gstv)
        Eval=Entry(box,text='Quantity cost',textvariable=cval)
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
        
        def fetch():
            t=eic.get()
            con=sqlite3.connect('MSW.db')
            try:
                stkd=con.execute("select description,hsn,gst,price,units,utype from stock where itemcode is %s"%(t))
                d=stkd.fetchall()
                desc.set(d[0][0])
                hsn.set(d[0][1])
                gst.set(d[0][2])
                price.set(d[0][3])
                gstv.set(round((gst.get()/100)*price.get(),2))
                q.set(d[0][4])
                qt.set(d[0][5])
            except:
                messagebox.showinfo(parent=box,title='Error',message="Wrong input")
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
        Eqreq=Entry(box,text='Quantity Required',validate="key")
        Eqreq['validatecommand']=(Eqreq.register(val),'%P','%d')
        Eqreq.grid(row=10,column=4)
        fetchb=Button(box,text='Fetch details',command=fetch)
        fetchb.grid(row=0,column=2,ipadx=2,ipady=5)
        def addcheck():
            if int(Eqreq.get()) <= int(q.get()):
                #command to add to bill
                print ('Success')
                return
            else:
                messagebox.showinfo(parent=box,title='Error',message='Quantity not available !! check entry')
                return
        addb=Button(box,text="Add",command=addcheck)
        addb.grid(row=12,column=6)
        
        return
    
    

def MainWindow():
    bw=billwindow()
    bbox=Tk()
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
    Lcd=Label(frame1,text="Enter Customer Detail")
    Lcd.grid(row=1,column=0)
    Ecd=Entry(frame1,text="Customer Detail",bd=10,validate='key',width=40)
    Ecd['validatecommand']=(Ecd.register(Val),'%d',41,'%P')
    Ecd.grid(row=1,column=1)
    Lan=Label(frame1,text="\tEnter Aadhaar Number")
    Lan.grid(row=1,column=2)
    Ean=Entry(frame1,text="Aadhar Number",bd=10,validate='key',width=13)
    Ean['validatecommand']=(Ean.register(intval),'%d',13,'%P')
    Ean.grid(row=1,column=3)
    Ldr=Label(frame1,text="\tDate :")
    Ldr.grid(row=1,column=4)
    Ld=Label(frame1,text=datetime.date.today().strftime("%d-%m-%Y"))
    Ld.grid(row=1,column=5)
    Lb=Label(frame1,text="\tBill Number :")
    Lb.grid(row=1,column=6)
    Lbn=Label(frame1,text="DDMMYYYYXXXX")
    Lbn.grid(row=1,column=7)
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
    Lsn=Label(frame2,text="S.No")
    Lsn.grid(row=0,column=0)
    Lic=Label(frame2,text="Item Code")
    Lic.grid(row=0,column=1,ipadx=20)
    Ld=Label(frame2,text="Description")
    Ld.grid(row=0,column=2,ipadx=20)
    Lhsn=Label(frame2,text="HSN")
    Lhsn.grid(row=0,column=3,ipadx=20)
    Lqty=Label(frame2,text="Qty")
    Lqty.grid(row=0,column=4,ipadx=20)
    Lprice=Label(frame2,text="Price per qty")
    Lprice.grid(row=0,column=5,ipadx=20)
    Lcgst=Label(frame2,text="CGST")
    Lcgst.grid(row=0,column=6,ipadx=20)
    Lsgst=Label(frame2,text="SGST")
    Lsgst.grid(row=0,column=7,ipadx=20)
    Ltot=Label(frame2,text="Total")
    Ltot.grid(row=0,column=8,ipadx=20)
    rn=0
    cn=8
    
    frameb=Frame(bbox,height=200)
    frameb.pack(side='bottom')
    add=Button(frameb,text='Add Item',command=lambda w=frameb,rn=rn,cn=cn:bw.addproduct(w,rn,cn))
    add.grid(row=0,column=2,padx=500)
    billphoto=PhotoImage(file='bill.png')
    billitem=Button(frameb,image=billphoto)
    billitem.grid(row=1,column=1,padx=10,pady=10)
    tv=123#amount to be paid in total
    tv=str(tv)
    Lc=Label(frameb,text=str('Payable Amount\t\tRs.'+tv))
    Lc.grid(row=1,column=2,padx=0)
    def ex():
        bbox.destroy()
    Ex=Button(frameb,text='Exit',command=ex)
    Ex.grid(row=2,column=3,padx=5,pady=10)
    bbox.mainloop()
    
MainWindow()
