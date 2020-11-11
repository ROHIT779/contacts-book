# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 21:54:23 2020

@author: User
"""

from tkinter import *
from tkinter import ttk
import mysql.connector
window=Tk()
window.title("Contacts book")
window.geometry("720x404")


mydb=mysql.connector.connect(host=,user=,passwd=)
print(mydb)
mc=mydb.cursor()
mc.execute("USE contacts_book")
mc.execute("DESCRIBE contacts")
for x in mc:
    print(x)
    


    
    
def ok_btn_fn():
    name=add_txt1.get()
    phn=int(add_txt2.get())
    print(name)
    print(phn)
    if name=="":
        no_name=Label(tab1,text="Error: No name selected")
        no_name.grid(row=4,column=1)
        no_name.after(3000,no_name.destroy)
        return
    sql=mc.execute("INSERT INTO contacts VALUES ('%s','%d')"%(name,phn))
    ok_success=Label(tab1,text="Added Successfully")
    ok_success.grid(row=4,column=1)
    ok_success.after(1000,ok_success.destroy)
    mydb.commit()
    
def cancel_btn_fn():
    add_txt1.delete(0,'end')
    add_txt2.delete(0,'end')



tab_control=ttk.Notebook(window)
tab1=ttk.Frame(tab_control)
tab2=ttk.Frame(tab_control)
tab3=ttk.Frame(tab_control)
tab4=ttk.Frame(tab_control)
tab_control.add(tab1,text="Add",)
tab_control.add(tab2,text="View")
tab_control.add(tab3,text="Delete")
tab_control.add(tab4,text="Search")


add_lbl1=Label(tab1,text="Name: ")
add_txt1=Entry(tab1,width=20)
add_lbl2=Label(tab1,text="Phone: ")
add_txt2=Entry(tab1,width=20)
add_lbl1.grid(row=2,column=0)
add_txt1.grid(row=2,column=1)
add_lbl2.grid(row=2,column=2)
add_txt2.grid(row=2,column=3)

ok_btn=Button(tab1,text="Ok",command=ok_btn_fn)
cancel_btn=Button(tab1,text="Cancel",command=cancel_btn_fn)
ok_btn.grid(row=3,column=0)
cancel_btn.grid(row=3,column=1)


def view_fn():
    
    listbox_view.delete(0,END)
    mc.execute("SELECT * FROM contacts")
    i=3
    for row in mc:
        nm=str(row[0])
        phn=str(row[1]).rjust(40)
        listbox_view.insert(END,"%s%s"%(nm,phn))
        i+=1
    lbl5=Label(tab2,text="%d Results"%(i-3))
    lbl5.grid(row=1)


yscrollbar_view=Scrollbar(tab2)
yscrollbar_view.grid(row=3,column=2)
listbox_view=Listbox(tab2,width=60,height=10,yscrollcommand=yscrollbar_view.set)
listbox_view.grid(row=3,column=1)
yscrollbar_view.config(command=listbox_view.yview) 
  
lbl3=Label(tab2,text="Name")
lbl4=Label(tab2,text="Phone")
lbl3.grid(row=2,column=1)
lbl4.grid(row=2,column=2)
view_btn=Button(tab2,text="View",command=view_fn)
view_btn.grid(row=0,column=1)


def del_btn_fn():
    nm=(del_txt.get(),)
    sql="DELETE FROM contacts WHERE name=%s"
    mc.execute(sql,nm)
    mydb.commit()
    del_success=Label(tab3,text="Deleted Successfully")
    del_success.grid(row=4,column=1)
    del_success.after(1000,del_success.destroy)

def clear_all_fn():
    sql="DELETE FROM contacts"
    mc.execute(sql)
    mydb.commit()
    del_all_success=Label(tab3,text="Deleted all contacts")
    del_all_success.grid(row=4,column=1)
    del_all_success.after(1000,del_all_success.destroy)

del_lbl=Label(tab3,text="Enter Name: ")
del_txt=Entry(tab3,width=30)
del_btn=Button(tab3,text="Delete",command=del_btn_fn)
del_lbl.grid(row=1,column=1)
del_txt.grid(row=1,column=2)
del_btn.grid(row=2,column=1)
clear_all_btn=Button(tab3,text="Delete All Contacts",command=clear_all_fn)
clear_all_btn.grid(row=2,column=2)


def srch_btn_fn():
    listbox_srch.delete(0,END)
    srch_nm=(srch_txt.get()+"%",)
    print(srch_nm)
    sql="SELECT name,phone_number FROM contacts WHERE name LIKE %s"
    mc.execute(sql,srch_nm)
    srch_results=mc.fetchall()
    nm=Label(tab4,text="Name")
    ph=Label(tab4,text="Phone")
    nm.grid(row=3,column=1)
    ph.grid(row=3,column=2)
    i=4
    
    for row in srch_results:
        n=str(row[0])
        p=str(row[1]).rjust(40)
        listbox_srch.insert(END,"%s%s"%(n,p))
        i+=1


    lbl6=Label(tab4,text="%d Results"%(i-4))
    lbl6.grid(row=2)

yscrollbar_srch=Scrollbar(tab4)
yscrollbar_srch.grid(row=4,column=2)
listbox_srch=Listbox(tab4,width=60,height=10,yscrollcommand=yscrollbar_srch.set)
listbox_srch.grid(row=4,column=1)
yscrollbar_srch.config(command=listbox_srch.yview)

srch_lbl=Label(tab4,text="Enter Name: ")
srch_txt=Entry(tab4,width=30)
srch_btn=Button(tab4,text="Search",command=srch_btn_fn)
srch_lbl.grid(row=0,column=1)
srch_txt.grid(row=0,column=2)
srch_btn.grid(row=1,column=1)


tab_control.pack(expand=1,fill='both')
window.mainloop()