from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
from PIL import ImageTk,Image                   #pip install pillow
import numpy as np
from matplotlib import pyplot as plt
import requests
import bs4
from io import BytesIO
import socket


#SPLASH WINDOW

root1 = Tk()                                    ######SPLASH SCREEN PART
root1.title("SPLASH SCREEN")
root1.geometry("1000x1600")

T = Text(root1, height=1, width=60, pady=10)
T.pack()

#TEMPRATURE CODE

try:
    city="Mumbai"
    socket.create_connection(("www.google.com",80))
    a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
    a2="&q=" + city
    a3="&appid=a2c5dcc14dfeaab1005d6787fbedc58b"
    api_address=a1+a2+a3
    res1=requests.get(api_address)
    print(res1)
    wdata = requests.get(api_address).json()
    main=wdata['main']
    temp=main['temp']
except OSError:
    messagebox.showerror("Network","Check Network")

T.insert(END, "Current Temprature of Mumbai :-")
T.insert(END, temp)
T.insert(END, ' Degree')
T.config(state=DISABLED)                    #it disables the editing of the text makes it only readable

#QUOTE OF THE DAY CODE

res=requests.get("https://www.brainyquote.com/quotes_of_the_day.html/")
print(res)
soup = bs4.BeautifulSoup(res.text,'lxml')
quote=soup.find('img',{"class":"p-qotd"})
a=('https://www.brainyquote.com' + quote['data-img-url'])


img_url=a
response = requests.get(img_url)
img_data = response.content
img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
panel = Label(root1, image=img)
panel.pack()


root1.after(5000, lambda: root1.destroy())       #destroys the screen after 5 seconds and time is in milli seconds
root1.mainloop()

#MAIN WINDOW

root = Tk()                                      ######NEXT WINDOW PART
root.title("PYTHON PROJECT")
root.geometry("500x500+100+100")


def f1():
    root.withdraw()
    adst.deiconify()
    entAddRno.focus()
    

def f3():
	vist.deiconify()
	root.withdraw()
	con =None
	cursor = None
	try:
		con = cx_Oracle.connect("system/abc123")
		cursor = con.cursor()
		sql = "select * from student" 
		cursor.execute(sql)
		data = cursor.fetchall()
		msg= ''
		for d in data:
			msg= msg + "Roll No:-"+ str(d[0])+ "  Name:-"+ str(d[1])+ "  Marks:-"+ str(d[2])+ "\n"
		stData.config(state=NORMAL)              #makes the text normal for editing
		stData.delete('1.0','end')               #removes all the precious data on the text and makes it blank
		stData.insert(INSERT, msg)               #insert the data
		stData.config(state=DISABLED)            #disabled the state and makes it read-only
			
	except 	cx_Oracle.DatabaseError as e:
		con.rollback()
		

	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

def f8():
    root.deiconify()
    query='SELECT name,marks FROM student'
    name =  []
    marks = []


    #connect to database and execute query.
    db = cx_Oracle.connect('system', 'abc123', 'localhost:1521/XE')
    cursor = db.cursor()
    cursor.execute(query)

    #loop through the rows fetched and store the records as arrays.
    for row in cursor:
        name.append(row[0])
        marks.append(row[1])

    #plot the bar chart
    x=np.arange(len(name))
    plt.bar(x,marks,width=0.25)
    plt.bar(name,marks)
    plt.show()

def f6():
    delst.deiconify()
    root.withdraw()
    entAddRnoo.focus()

def f9():
    upst.deiconify()
    root.withdraw()
    entAddRnooo.focus()

btnAdd = Button(root, text="Add", width=20, command=f1)
btnView = Button(root, text="View", width=20, command=f3)
btnUpdate = Button(root, text="Update", width=20, command=f9)
btnDelete = Button(root, text="Delete", width=20, command=f6)
btnGraph = Button(root, text="Graph", width=20, command=f8)

btnAdd.pack(pady=20)
btnView.pack(pady=20)
btnUpdate.pack(pady=20)
btnDelete.pack(pady=20)
btnGraph.pack(pady=20)


#ADD STUDENT

adst = Toplevel(root)
adst.title("Add Student Info")
adst.geometry("500x500+100+100")
adst.withdraw()

def f2():
    adst.withdraw()
    root.deiconify()

def f5():
    con = None
    cursor = None
    try:
        con = cx_Oracle.connect("system/abc123")
        srno = entAddRno.get()
        if srno.isdigit() and int(srno)>0:
            rno = int(srno)
        else:
            messagebox.showerror("MISTAKE","Incorrect Roll No.")
            entAddRno.delete(0,END)
            entAddRno.focus()
            return
        
        sname = entAddName.get()
        if sname.isdigit():
            messagebox.showerror("MISTAKE","Enter Valid Name")
            entAddName.delete(0,END)
            entAddName.focus()
            return
        else:
            name = sname
        
        smarks = entAddMarks.get()
        if smarks.isdigit() and int(smarks)>0 and int(smarks)<101:
            marks = int(smarks)
        else:
            messagebox.showerror("MISTAKE","Enter Valid Marks")
            entAddMarks.delete(0,END)
            entAddMarks.focus()
            return
        
        sql = "insert into student values ('%d','%s','%d')"
        args = (rno,name,marks)
        cursor = con.cursor()
        cursor.execute(sql % args)
        con.commit()
        msg = str(cursor.rowcount)+" Records Entered"
        messagebox.showinfo("Success", msg)
    except cx_Oracle.DatabaseError as e:
        con.rollback()
        messagebox.showerror(" Wrong", "Roll No. Already Exixts")
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()
    

lblAddRno = Label(adst, text="Enter Roll No. ")
entAddRno = Entry(adst, bd=5)
lblAddName = Label(adst, text="Enter Name ")
entAddName = Entry(adst, bd=5)
lblAddMarks = Label(adst, text="Enter the marks")
entAddMarks = Entry(adst, bd=5)

btnAddSave = Button(adst, text="Save", command=f5)
btnAddBack = Button(adst, text="Back", command=f2)

lblAddRno.pack()
entAddRno.pack()
lblAddName.pack()
entAddName.pack()
lblAddMarks.pack()
entAddMarks.pack()

btnAddSave.pack(pady=10)
btnAddBack.pack()

#VIEW STUDENT

vist = Toplevel(root)
vist.title("View Student Info")
vist.geometry("500x500+100+100")
vist.withdraw()

def f4():
    vist.withdraw()
    root.deiconify()
    stData.delete(1.0, END)


stData = scrolledtext.ScrolledText(vist, width=40, height=10)
btnViewBack = Button(vist, text="Back", command=f4)
stData.pack()
btnViewBack.pack(pady=10)


#DELETE STUDENT

delst=Toplevel(root)
delst.title("Delete Student Info")
delst.geometry("500x500+100+100")
delst.withdraw()

def f7():
    delst.withdraw()
    root.deiconify()

def f10():
    con =None
    cursor = None
    try:
            con = cx_Oracle.connect("system/abc123")
            srno = entAddRnoo.get()
            if srno.isdigit() and int(srno)>0:
                rno=int(srno)
            else:
                messagebox.showerror("Mistake","Incorrect Roll No")
                entAddRnoo.delete(0,END)
                entAddRnoo.focus()
                return
                
            cursor = con.cursor()
            sql = "delete from student where rno='%d'"
            args = (rno)
            cursor.execute(sql % args)
            con.commit()
            msg = str(cursor.rowcount) + " Deleted"
            if int(cursor.rowcount)>0:
                messagebox.showinfo("Sucess", msg)
            else:
                messagebox.showerror("Failure","Wrong Info Entered")
                return
    except cx_Oracle.DatabaseError as e:
            con.rollback()
            messagebox.showerror("Failure", e)
    finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
    
lblAddRnoo = Label(delst, text="Enter Roll No. ")
entAddRnoo= Entry(delst, bd=5)
btnAddDelete = Button(delst, text="Delete", command=f10)
btnAddBack = Button(delst, text="Back", command=f7)

lblAddRnoo.pack()
entAddRnoo.pack()
btnAddDelete.pack(pady=10)
btnAddBack.pack(pady=10)

#UPDATE STUDENT

upst = Toplevel(root)
upst.title("Update Student Info")
upst.geometry("500x500+100+100")
upst.withdraw()


def f11():
    root.deiconify()
    upst.withdraw()

def f12():
    con = None
    cursor = None
    try:
        con = cx_Oracle.connect("system/abc123")
        srno = entAddRnooo.get()
        if srno.isdigit() and int(srno)>0:
            rno = int(srno)
        else:
            messagebox.showerror("MISTAKE","Incorrect Roll No.")
            entAddRnooo.delete(0,END)
            entAddRnooo.focus()
            return
        
        sname = entAddNamee.get()
        if sname.isdigit():
            messagebox.showerror("MISTAKE","Enter Valid Name")
            entAddNamee.delete(0,END)
            entAddNamee.focus()
            return
        else:
            name = sname
        
        smarks = entAddMarkss.get()
        if smarks.isdigit() and int(smarks)>0 and int(smarks)<101:
            marks = int(smarks)
        else:
            messagebox.showerror("MISTAKE","Enter Valid Marks")
            entAddMarkss.delete(0,END)
            entAddMarkss.focus()
            return
        
        sql = "update student set name='%s', marks='%d' where rno='%d'"
        args = (name,marks,rno)
        cursor = con.cursor()
        cursor.execute(sql % args)
        con.commit()
        msg = str(cursor.rowcount)+" Records Updated"
        if int(cursor.rowcount)>0:
                messagebox.showinfo("Sucess", msg)
        else:
                messagebox.showerror("Failure","Roll No. Entered Does Not Exists")
                return
        messagebox.showinfo("Success", msg)
    except cx_Oracle.DatabaseError as e:
        con.rollback()
        messagebox.showerror(" Wrong", e)
    finally:
        if cursor is not None:
            cursor.close()
        if con is not None:
            con.close()
    
    

lblAddRnooo = Label(upst, text="Enter Roll No. ")
entAddRnooo = Entry(upst, bd=5)
lblAddNamee = Label(upst, text="Enter Name ")
entAddNamee = Entry(upst, bd=5)
lblAddMarkss = Label(upst, text="Enter the marks")
entAddMarkss = Entry(upst, bd=5)

btnAddSave = Button(upst, text="Save", command=f12)
btnAddBack = Button(upst, text="Back", command=f11)

lblAddRnooo.pack()
entAddRnooo.pack()
lblAddNamee.pack()
entAddNamee.pack()
lblAddMarkss.pack()
entAddMarkss.pack()

btnAddSave.pack(pady=10)
btnAddBack.pack()


root.mainloop()
