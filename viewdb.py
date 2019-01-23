import sqlite3
from tkinter import *

def viewdbtable():
    db=sqlite3.connect('test.db')
    cur=db.execute("select * from company")
    box=Tk()
    frame=Frame(box)
    
    for d in cur:
        print (d)
    #print ([d[0] for d in cur.description])
    #print ([d for d in cur])
    return 

def griduse(root):
    con=sqlite3.connect('test.db')
    cursor=con.execute("select * from company")
    #root = Tk()
    #root.geometry("500x500")
    i=0
    j=1
    l=[d[0] for d in cursor.description]
    def pri(i,j):
        #code you want the button to do
        s='company'
        con=sqlite3.connect('test.db')
        cursor=con.execute("select * from %s"%(s))
        val=[d[0] for d in cursor]
        l=[d[0] for d in cursor.description]
        l1=l[0]#parameter name(column name to be compared)
        v=val[i-1]#contains the parameter value to be compared
        print(i,l1,v)
        b=con.execute("select * from %s where %s=?"%(s,l1),(v,))#selected row
        for a in b:
            print (a)
        con.close()
        
            
    for v in l:
        t=Label(root,text=v,fg='black',bd=5)
        t.grid(row=i,column=j)
        j=j+1
    for r in cursor:#Rows
        i=i+1
        j=0
        n=Label(root,text=i,fg='black')
        n.grid(row=i,column=j)
        j=j+1
        for c in r: #Columns
            e = Entry(root,fg='green')
            e.grid(row=i, column=j)
            e.insert(i,c)
            e.configure(state=NORMAL)               
            j=j+1

        b=Button(root,text='update',command=lambda row=i,column=j:pri(row,column))
        b.grid(row=i,column=j)
    con.close()
    return()

def window():
    root =Tk()
    root.geometry("500x500")
    canvas=Canvas(root,borderwidth=0)
    frame=Frame(canvas)
    vsb=Scrollbar(root,orient="vertical",command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right",fill='y')
    canvas.pack(side="left",fill="both",expand=True)
    canvas.create_window((4,4),window=frame,anchor="nw")
    def onFrameConfigure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
    frame.bind("<Configure>",lambda event,canvas=canvas: onFrameConfigure(canvas))
    griduse(frame)
    mainloop()
    return

window()
#griduse()
#viewdbtable()

