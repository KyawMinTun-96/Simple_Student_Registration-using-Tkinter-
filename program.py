import pymysql
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox


root = Tk()
root.title("Student Registration")
root.geometry("960x720")
root.configure(bg="lightgray")
my_tree = ttk.Treeview(root)

stuid = tk.StringVar()
fname = tk.StringVar()
lname = tk.StringVar()
phone = tk.StringVar()
address = tk.StringVar()


def setph(word,num):
    if num ==1:
        stuid.set(word)
    if num ==2:
        fname.set(word)
    if num ==3:
        lname.set(word)
    if num ==4:
        phone.set(word)
    if num ==5:
        address.set(word)

# ===================For Function=========================
def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='student_db'
    )

    return conn

def refreshTable():
    for data in my_tree.get_children():
        res = my_tree.delete(data)

    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)




def add():

    stuid = str(stuEntry.get())
    fname = str(fnameEntry.get())
    lname = str(lnameEntry.get())
    phone = str(phoneEntry.get())
    address = str(addressEntry.get())

    if(stuid == "" or stuid == " ") or (fname == "" or fname == " ") or (lname == "" or lname == " ") or (phone == "" or phone == " ") or (address == "" or address == " "):

        messagebox.showinfo("Error", "Please fill up information!")

    else:

        try:
            con = connection()

            if con.connect:

                cursor = con.cursor()
                cursor.execute("INSERT INTO student (student_id, firstname, lastname, phone, address) VALUES ('"+stuid+"', '"+fname+"', '"+lname+"', '"+phone+"', '"+address+"')")
                con.commit()
                con.close()
                messagebox.showinfo("Alert", "Successfully Saved!")
                refreshTable()
        except Exception as e:
            print(e)

def reset():
    ask = messagebox.askquestion("Warnning!", "Delete all data?")

    if ask != "yes":
        return
    else:
        try:
            print(ask)
            con = connection()
            
            if con.connect:
                cursor = con.cursor()
                cursor.execute("DELETE FROM student")
                con.commit()
                con.close()
                messagebox.showinfo("Info!", "Successfully deleted!")
                refreshTable()
            else:
                messagebox.showinfo("Error", "Sorry an error occured")

        except:
            messagebox.showinfo("Error", "Sorry an error occured")
            return

def update():
    select_id = ""
    select_item = my_tree.selection()[0]
    select_id = str(my_tree.item(select_item)['values'][0])

    stuid = str(stuEntry.get())
    fname = str(fnameEntry.get())
    lname = str(lnameEntry.get())
    phone = str(phoneEntry.get())
    address = str(addressEntry.get())
    

    if(stuid == "" or stuid == " ") or (fname == "" or fname == " ") or (lname == "" or lname == " ") or (phone == "" or phone == " ") or (address == "" or address == " "):

        messagebox.showinfo("Error", "Please fill up information!")

    else:
        try:
            con = connection()
            if con.connect:
                cursor = con.cursor()
                cursor.execute("UPDATE student SET student_id='"+stuid+"', firstname='"+fname+"', lastname='"+lname+"', phone='"+phone+"', address='"+address+"' WHERE  student_id='"+select_id+"'")
                con.commit()
                con.close()
                messagebox.showinfo("Info!", "Successfully Updated!")
                refreshTable()

        except Exception as e:
            print(e)

def delete():
    ask = messagebox.askquestion("Warnning!", "Delete all data?")

    if ask != "yes":
        return

    else:
        select_id = ""
        select_item = my_tree.selection()[0]
        select_id = str(my_tree.item(select_item)['values'][0])

        try:
            con = connection()
            if con.connect:
                cursor = con.cursor()
                cursor.execute("DELETE FROM student WHERE student_id='"+select_id+"'")
                con.commit()
                con.close()
                messagebox.showinfo("Info", "Successfully deleted selected item!")
                refreshTable()

        except Exception as e:
            print(e)

def select():
    try:
        selected_item = my_tree.selection()[0]
        studid = str(my_tree.item(selected_item)['values'][0])
        fname = str(my_tree.item(selected_item)['values'][1])
        lname = str(my_tree.item(selected_item)['values'][2])
        phone = str(my_tree.item(selected_item)['values'][3])
        address = str(my_tree.item(selected_item)['values'][4])

        setdata(studid, 1)
        setdata(fname, 2)
        setdata(lname, 3)
        setdata(phone, 4)
        setdata(address, 5)

    except Exception as e:
        print(e)

def setdata(word, num):
    if(num == 1):
        stuid.set(word)
    if(num == 2):
        fname.set(word)
    if(num == 3):
        lname.set(word)
    if(num == 4):
        phone.set(word)
    if(num == 5):
        address.set(word)

def search():

    stuid = str(stuEntry.get())
    fname = str(fnameEntry.get())
    lname = str(lnameEntry.get())
    phone = str(phoneEntry.get())
    address = str(addressEntry.get())

    con = connection()
    if con.connect:

        cursor = con.cursor()
        cursor.execute("SELECT * FROM student WHERE student_id ='"+stuid+"' or firstname = '"+fname+"' or lastname = '"+phone+"' or address = '"+address+"'")

        try:
            result = cursor.fetchall()

            for num in range(0, 5):
                setdata(result[0][num], (num+1))

            con.commit()
            con.close()
        except Exception as e:
            print(e)
            return

def read():
    conn = connection()
    
    if conn.connect:

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        results = cursor.fetchall()
        conn.commit()
        conn.close()

    return results
print (read())




label = Label(root, bg="lightgray", text="Student Registration", font=("Sans-Serif Bold", 30))
label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=40)

#====================For Label=======================
stuidLabel = Label(root, bg="lightgray", text="Student ID:", font=("Calibri", 15))
fnameLabel = Label(root, bg="lightgray", text="First Name:", font=("Calibri", 15))
lnameLabel = Label(root, bg="lightgray", text="Last Name:", font=("Calibri", 15))
phoneLabel = Label(root, bg="lightgray", text="Phone:", font=("Calibri", 15))
addressLabel = Label(root, bg="lightgray", text="Address:", font=("Calibri", 15))

stuidLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5, sticky=W)
fnameLabel.grid(row=4, column=0, columnspan=1, padx=50, pady=5, sticky=W)
lnameLabel.grid(row=5, column=0, columnspan=1, padx=50, pady=5, sticky=W)
phoneLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5, sticky=W)
addressLabel.grid(row=7, column=0, columnspan=1, padx=50, pady=5, sticky=W)




# ===================For Entry=========================
stuEntry = Entry(root, width=55, bd=5, font=("Calibri", 15), textvariable=stuid)
fnameEntry = Entry(root, width=55, bd=5, font=("Calibri", 15), textvariable=fname)
lnameEntry = Entry(root, width=55, bd=5, font=("Calibri", 15), textvariable=lname)
phoneEntry = Entry(root, width=55, bd=5, font=("Calibri", 15), textvariable=phone)
addressEntry = Entry(root, width=55, bd=5, font=("Calibri", 15), textvariable=address)

stuEntry.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
fnameEntry.grid(row=4, column=1, columnspan=4, padx=5, pady=0)
lnameEntry.grid(row=5, column=1, columnspan=4, padx=5, pady=0)
phoneEntry.grid(row=6, column=1, columnspan=4, padx=5, pady=0)
addressEntry.grid(row=7, column=1, columnspan=4, padx=5, pady=0)


# ===================For Button=========================
addBtn = Button(root, padx=15, pady=5, width=10, bd=5, font=("Calibri", 15), fg="#fff", bg="#20df42", text="Add", command=add)
updateBtn = Button(root, padx=15, pady=5, width=10, bd=5, font=("Calibri", 15), fg="#fff", bg="#0960ca", text="Update", command=update)
deleteBtn = Button(root, padx=15, pady=5, width=10, bd=5, font=("Calibri", 15), fg="#fff", bg="red", text="Delete", command=delete)
resetBtn = Button(root, padx=15, pady=5, width=10, bd=5, font=("Calibri", 15), fg="#000", bg="#fff", text="Reset", command=reset)
searchBtn = Button(root, padx=15, pady=5, width=10, bd=5, font=("Calibri", 15), fg="#000", bg="lightblue", text="Search", command=search)
selectBtn = Button(root, padx=15, pady=25, width=10, bd=5, font=("Calibri", 15), fg="#fff", bg="gray", text="Select", command=select)

addBtn.grid(row=3, column=5, columnspan=1, rowspan=2)
updateBtn.grid(row=5, column=5, columnspan=1, rowspan=2)
deleteBtn.grid(row=7, column=5, columnspan=1, rowspan=2)
resetBtn.grid(row=9, column=5, columnspan=1, rowspan=2)
searchBtn.grid(row=11, column=5, columnspan=1, rowspan=2)
selectBtn.grid(row=13, column=5, columnspan=1, rowspan=2)




# ===================For Table=========================
style = ttk.Style()
style.configure("Treeview.Heading", font=('Calibri Bold', 15))

my_tree['columns'] = ("Stud ID","Firstname","Lastname","Phone","Address")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Stud ID", anchor=W, width=170)
my_tree.column("Firstname", anchor=W, width=150)
my_tree.column("Lastname", anchor=W, width=150)
my_tree.column("Phone", anchor=W, width=150)
my_tree.column("Address", anchor=W, width=165)

my_tree.heading("Stud ID", text="Student ID", anchor=W)
my_tree.heading("Firstname", text="Firstname", anchor=W)
my_tree.heading("Lastname", text="Lastname", anchor=W)
my_tree.heading("Phone", text="Phone", anchor=W)
my_tree.heading("Address", text="Address", anchor=W)


refreshTable()
root.mainloop()