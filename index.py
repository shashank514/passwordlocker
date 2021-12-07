import sqlite3, hashlib
from sqlite3.dbapi2 import Cursor
from tkinter import *
from tkinter import simpledialog
from functools import partial


with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()
    
    
cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS savepasswords(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")

window = Tk()

window.title("Password vault")





def popUp(text):
    answer = simpledialog.askstring("input string",text)

    return answer

def firstScreen():
    window.geometry("350x150")
    
    lbl = Label(window, text="Create Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()
    
    txt = Entry(window, width=10,show="*")
    txt.pack()
    txt.focus()
    
    
    lbl1 = Label(window, text="Re-enter Password")
    lbl1.pack()
    
    
    txt1 = Entry(window, width=10,show="*")
    txt1.pack()
    txt.focus()
    
    lbl2 = Label(window)
    lbl2.pack()
    
    def savePassword():
        if txt.get() == txt1.get() :
            hashpassword = txt.get()
            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?)"""
            cursor.execute(insert_password,[(hashpassword)])
            db.commit()
            
            passwordvault()
            
        else :
            txt.delete(0,'end')
            txt1.delete(0,'end')
            lbl2.config(text="Password is not matched")
            
    
    
    btn = Button(window, text="save" ,command=savePassword)
    btn.pack(pady=10)
    
    

def loginScreen():
    for widget in window.winfo_children():
        widget.destroy()


    window.geometry("350x150")
    
    lbl = Label(window, text="Enter Master Password")
    lbl.config(anchor=CENTER)
    lbl.pack()
    
    txt = Entry(window, width=10,show="*")
    txt.pack()
    txt.focus()
    
    lbl1 = Label(window)
    lbl1.pack()
    
    def getmasterpassword():
        checkmasterpassword = txt.get()
        cursor.execute("SELECT * FROM masterpassword WHERE id=1 AND password=?",[(checkmasterpassword)])
        return cursor.fetchall()

    
    def checkPassword():
        match = getmasterpassword()
        
        if match:
            passwordvault()
            
        else:
            txt.delete(0,'end')
            lbl1.config(text="wrong password")
    
    btn = Button(window, text="submit" ,command=checkPassword)
    btn.pack(pady=10)
    
def passwordvault():
    for widget in window.winfo_children():
        widget.destroy()
        
    window.geometry("700x200")
    
    lbl = Label(window, text="Password vault")
    lbl.config(anchor=CENTER)
    lbl.pack()

    lbl1 = Label(window, text="Enter the 1 for saving new Password")
    lbl1.pack()

    lbl2 = Label(window, text="Enter the 2 for Show the saving Password")
    lbl2.pack()

    txt = Entry(window, width=10)
    txt.pack()
    txt.focus()


    lbl3 = Label(window)
    lbl3.pack()


    def checkentery1():
        valu = txt.get()

        if valu == "1":
            addentery()

        elif valu == "2":
            showlist()

        else :
            lbl3.config(text="enter one number to move")
            



    btn = Button(window, text="submit" ,command=checkentery1)
    btn.pack(pady=10)
    


def addentery():
    text1 = "website"
    text2 = "username"
    text3 = "password"

    website = popUp(text1)
    username = popUp(text2)
    password = popUp(text3)

    insert_fields = """INSERT INTO savepasswords(website,username,password)
    VALUES(?,?,?)"""

    cursor.execute(insert_fields, (website,username,password))
    db.commit()

    passwordvault()


def removeentery(input):
    cursor.execute("DELETE FROM savepasswords WHERE id = ?",(input,))
    db.commit()

    passwordvault()




def showlist():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("750x500")

    lbl = Label(window,text="website")
    lbl.grid(row=1,column=0,padx=80,pady=10)
    # lbl1.pack(row=1,column=0,padx=80)
    lbl = Label(window,text="username")
    lbl.grid(row=1,column=1,padx=80,pady=10)
    # lbl2.pack(row=1,column=1,padx=80)
    lbl = Label(window,text="password")
    lbl.grid(row=1,column=2,padx=80,pady=10)
    # lbl3.pack(row=1,column=2,padx=80)
    

    cursor.execute("SELECT * FROM savepasswords")
    if(cursor.fetchall() != None):
        i=0
        while True:
            cursor.execute("SELECT * FROM savepasswords")
            array = cursor.fetchall()

            lbl1 = Label(window,text=(array[i][1]))
            lbl1.grid(column=0,row=i+2)
            lbl1 = Label(window,text=(array[i][2]))
            lbl1.grid(column=1,row=i+2)
            lbl1 = Label(window,text=(array[i][3]))
            lbl1.grid(column=2,row=i+2)


            btn = Button(window,text="Delete",command= partial(removeentery, array[i][0]))
            btn.grid(column=3,row=i+2,pady=10)

            i=i+1


            cursor.execute("SELECT * FROM savepasswords")
            if(len(cursor.fetchall()) <= i):     
                break










  
cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginScreen()
else:
    firstScreen()


window.mainloop()