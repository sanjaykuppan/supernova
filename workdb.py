import sqlite3
import os.path
from tkinter import *
from tkinter import messagebox
global z
z=0

#Definition to check db exists
def checkfile(fname):
    if(os.path.isfile(fname)):
        return True
    return False
#Definition for update button
def upddb(r,i,f,t,w):
    global z
    r.destroy()
    box=Toplevel(master=w)
    box.geometry("500x180")
    box.title("update record")
    canvas=Canvas(box)
    frame=Frame(canvas)
    hsb=Scrollbar(box,orient="horizontal",command=canvas.xview)
    canvas.configure(xscrollcommand=hsb.set)
    hsb.pack(side="bottom",fill='x')
    canvas.pack(side="top",fill='both',expand=True)
    canvas.create_window((4,4),window=frame,anchor="nw")
    def onFrameConfigure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
    frame.bind("<Configure>",lambda event,canvas=canvas:onFrameConfigure(canvas))
    con=sqlite3.connect(f)
    cur=con.execute("select * from %s "%(t))
    label=[d[0] for d in cur.description]
    l=label[0]#column name to be compared
    val=[d[0] for d in cur]
    ref=val[i-1]#value to be compared
    rn=0
    cn=1
    
    for v in label:#label
        ld=Label(frame,text=v,fg='black',bd=5)
        ld.grid(row=rn,column=cn)
        
        cn=cn+1
    temp=con.execute("select * from %s where %s=?"%(t,l),(ref,))#selected row from table
    rn=1
    cn=1
    entries=[]
    for a in temp:#update box entry widget creation
        c=0
        for z in a:
            if c==0:
                uv=z
                ld=Label(frame,text=z,fg='black')
                ld.grid(row=rn,column=cn)
                cn=cn+1
                c=1
            else:
                e=Entry(frame,fg='green')
                e.grid(row=rn,column=cn)
                e.insert(i,z)
                entries.append(e)
                cn=cn+1
    def upd():
        con=sqlite3.connect(f)
        uval=[e.get() for e in entries]
        global z
        rn=0
        cn=0
        l1=label[0]
        for l in label:
            if rn!=0:
                con.execute("update %s set %s = ? where %s = ?"%(t,l,l1),(uval[cn],uv,))
                con.commit()
                cn=cn+1
            rn=rn+1
        box.destroy()
        z=0
        messagebox.showinfo(parent=w,title="Success",message="Update successful")
        con.close()
        return 
    subbut=Button(frame,text="update",command=upd)
    subbut.grid(row=rn,column=cn)
    def ex():
        box.destroy()
        global z
        z=0
        return
    exbut=Button(frame,text="Exit",command=ex)
    exbut.grid(row=rn+1,column=cn)
    con.close()
    z=1
    return

#Definition to Delete column
def delc(root,row,fname,tname):
    global z
    con=sqlite3.connect(fname)
    cur=con.execute("select * from %s"%(tname))
    label=[d[0] for d in cur.description]
    l=label[0]#column name to be compared
    val=[d[0] for d in cur]
    ref=val[row-1]#value to be compared
    con.execute("delete from %s where %s=?"%(tname,l),(ref,))
    con.commit()
    messagebox.showinfo(parent=root,title="Success",message='Deleted ')
    root.destroy()
    z=0 
    return

#Definition to create main window
def Window(fname,tname,w):
    global z
    root=Tk()
    root.geometry("1000x500")
    root.title(tname)
    root.lift()
    canvas=Canvas(root)
    frame=Frame(canvas)
    vsb=Scrollbar(root,orient="vertical",command=canvas.yview)
    hsb=Scrollbar(root,orient="horizontal",command=canvas.xview)
    canvas.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
    vsb.pack(side="right",fill='y')
    hsb.pack(side="bottom",fill='x')
    canvas.pack(side="left",fill='both',expand=True)
    canvas.create_window((4,4),window=frame,anchor="nw")
    def onFrameConfigure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
    frame.bind("<Configure>",lambda event,canvas=canvas:onFrameConfigure(canvas))
    con=sqlite3.connect(fname)
    cur=con.execute("select * from %s"%(tname))
    i=0
    j=1
    desc=[d[0] for d in cur.description]
    for v in desc:#column names
        t=Label(frame,text=v,fg='black',bd=4)
        t.grid(row=i,column=j)
        j=j+1
    for r in cur:#rows
        i=i+1
        j=0
        n=Label(frame,text=i,fg='black')
        n.grid(row=i,column=j)
        j=j+1
        for c in r:#columns
            e=Label(frame,text=c,fg='green')
            e.grid(row=i,column=j)
            j=j+1
        b=Button(frame,text='SELECT',command=lambda w=w,r=root,row=i,f=fname,t=tname:upddb(r,row,f,t,w))
        b.grid(row=i,column=j)
        d=Button(frame,text='Delete',command=lambda r=root,row=i,f=fname,t=tname:delc(r,row,f,t))
        d.grid(row=i,column=j+1)
    def ex(root):
        global z
        z=0
        root.destroy()
        return
    b=Button(frame,text='Exit',command= lambda r=root:ex(r))
    b.grid(row=i+6,column=j+3)
    root.lift()
    con.close()
    root.mainloop()
    return

#code to view db
def view(fname,tname,w):#pass parameter filename,tablename,parent window
    if checkfile(fname):         
        root=Toplevel(master=w)
        root.geometry("900x500")
        root.title(tname)
        root.lift()
        canvas=Canvas(root)
        frame=Frame(canvas)
        hsb=Scrollbar(root,orient="horizontal",command=canvas.xview)
        vsb=Scrollbar(root,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        vsb.pack(side="right",fill='y')
        hsb.pack(side="bottom",fill='x')
        canvas.pack(side="left",fill='both',expand=True)
        canvas.create_window((4,4),window=frame,anchor="nw")
        def onFrameConfigure(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))
        frame.bind("<Configure>",lambda event,canvas=canvas:onFrameConfigure(canvas))
        con=sqlite3.connect(fname)
        cur=con.execute("select * from %s"%(tname))
        i=0
        j=1
        desc=[d[0] for d in cur.description]
        for v in desc:#column names
            t=Label(frame,text=v,fg='black',bd=4)
            t.grid(row=i,column=j)
            j=j+1
        for r in cur:#rows
            i=i+1
            j=0
            n=Label(frame,text=i,fg='black')
            n.grid(row=i,column=j)
            j=j+1
            for c in r:#columns
                e=Label(frame,text=c,fg='green')
                e.grid(row=i,column=j)
                j=j+1
        def ex(root):
            root.destroy()
            return
        b=Button(frame,text='Exit',command= lambda r=root:ex(r))
        b.grid(row=i+6,column=j+3)
        root.lift()
        con.close()
        root.mainloop()
        return
    else :
        messagebox.showinfo(parent=w,title="Error",message="No file exists")
        return
        


#main function to update
def update(fname,tname,w):#fname is file name and tname is table name in db
    global z
    if checkfile(fname):
        Window(fname,tname,w)
    else:
        messagebox.showinfo(title="Error",message="No file exists")
    while z:
        Window(fname,tname,w)
    return


