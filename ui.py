from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Treeview
from typing import Any
from tkcalendar import Calendar
from dataclasses import dataclass
from threading import Thread
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter
import pymongo
import conf

import numpy as np
import functions as func



@dataclass
class GlobalVariables:
    #database
    db : pymongo.database.Database

    #ui
    root_window : Tk



def connectDbAndReturnDb(string_mongodb):
    cluster = pymongo.MongoClient(string_mongodb, tlsInsecure=True)
    db = cluster["CovidDatabase"]
    db.list_collection_names()

    return db




def createLoginFrame():

    def inner_prendiCredenziali():
        return insert_string.get()

    def loginAndChangeFrame():
        try:
            credenziali = inner_prendiCredenziali()
            global_var.db = connectDbAndReturnDb(credenziali)
            label_error.pack_forget()
            frame_login.pack_forget()
            frame_menu.pack()

        except:
            label_error.pack()
        return

    frame_login = Frame(global_var.root_window, bg = "white")
    label_error = Label(frame_login, text="Login Error", font='Arial 25', background="white", foreground="red")

    img = Image.open('images\\covid.jpg')
    img = img.resize((200, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(frame_login, image=img, background='white')
    panel.image = img
    panel.pack()

    label_string = Label(frame_login, text="Insert the string of the db:", font='Arial 15', foreground="green", background="white", pady=20)
    label_string.pack()
    insert_string = Entry(frame_login, font="Arial 8", width=100)
    insert_string.insert(0, conf.string_mongodb)
    insert_string.pack(pady=20)

    button_login = Button(frame_login, text="Login", command=loginAndChangeFrame, pady=15, padx=55)
    button_login.pack()

    button_quit = Button(frame_login, text="Quit", background= 'yellow', command=quit, pady=15, padx=58)
    button_quit.pack()

    return frame_login


def createRootWindow():
    root = Tk()
    root.title("CERTIFICATE DATABASE")
    root.geometry("800x800")
    root.configure(background="white")
    titolo = Label(root, text="SMBUD DELIVERY 2: MONGODB",font="Arial 30" ,background="white")
    titolo.pack()
    sottotitolo = Label(root, text="Giuseppe Urso, Simone Reale, Hazem Shalby, Marco Somaschini, Andrea Vitobello", font="Times 15" ,background="white", foreground="green")
    sottotitolo.pack()
    return root




#frame reale
def createFrame1():
    def goToMenu():
        frame1.pack_forget()
        frame_menu.pack()
        return

    frame1 = Frame(global_var.root_window, bg="white")
    label_frame1 = Label(frame1, text="FRAME 1 REALE", font="20", background="white", pady=20)
    label_frame1.pack()
    go_to_menu = Button(frame1, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame1




#frame shalby
def createFrame2():
    def goToMenu():
        frame2.pack_forget()
        frame_menu.pack()
        return
  
    frame2 = Frame(global_var.root_window, bg="white")
    label_frame2 = Label(frame2, text="FRAME 2 SHALBY", font="Arial 20", background="white", pady=10)
    label_frame2.pack()
    go_to_menu = Button(frame2, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame2




#frame somaschini
def createFrame3():

    def goToMenu():
        frame3.pack_forget()
        frame_menu.pack()
        return

    frame3 = Frame(global_var.root_window, bg="white")
    label_frame3 = Label(frame3, text="FRAME 3 SOMASCHINI", font="20", background="white", pady=20)
    label_frame3.pack()
    go_to_menu = Button(frame3, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame3



#frame urso
def createFrame4():
    def goToMenu():
        frame4.pack_forget()
        frame_menu.pack()
        return

    frame4 = Frame(global_var.root_window, bg="white")
    label_frame4 = Label(frame4, text="FRAME 4 URSO", font="20", background="white", pady=20)
    label_frame4.pack()
    go_to_menu = Button(frame4, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame4




#frame vitobello
def createFrame5():
    def goToMenu():
        frame5.pack_forget()
        frame_menu.pack()
        return

    frame5 = Frame(global_var.root_window, bg="white")
    label_frame5 = Label(frame5, text="FRAME 5 VITOBELLO", font="20", background="white", pady=20)
    label_frame5.pack()
    go_to_menu = Button(frame5, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()

    return frame5




#frame urso
def createFrame9():
    def goToMenu():
        frame9.pack_forget()
        frame_menu.pack()
        return


    frame9 = Frame(global_var.root_window, bg="white")
    label_frame9 = Label(frame9, text="FRAME 9 URSO", font="20", background="white", pady=20)
    label_frame9.pack()
    go_to_menu = Button(frame9, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame9




#frame vitobello2
def createFrame10():
    def goToMenu():
        frame10.pack_forget()
        frame_menu.pack()
        return

    frame10 = Frame(global_var.root_window, bg="white")
    label_frame10 = Label(frame10, text="FRAME 10 VITOBELLO", font="20", background="white", pady=20)
    label_frame10.pack()
    go_to_menu = Button(frame10, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame10



def createDatasetFrame():
    def goToMenu():
        createDatasetFrame.pack_forget()
        frame_menu.pack()
        return

    def create():
        t = Thread(target=func.createDataset, args=(scale_pop.get(), global_var.db))
        t.start()
        return

    def deleteAll():
        t = Thread(target=deleteAllSub)
        t.start()
        return

    def deleteAllSub():
        col_authBod = global_var.db['AuthorizedBodies_Collection']
        col_cert = global_var.db['Certificate_Collection']
        col_authBod.delete_many({})
        col_cert.delete_many({})

    createDatasetFrame = Frame(global_var.root_window, bg="white")
    label_createpopframe = Label(createDatasetFrame, text="CREATE DATASET: NUMBER OF PEOPLE", font="20", background="white", pady=20)
    label_createpopframe.pack()
    scale_pop = Scale(createDatasetFrame, from_=10, to=100, orient="horizontal", background="white", length=200, cursor="plus", font="Arial 15")
    scale_pop.set(50)
    scale_pop.pack(pady=15)
    button_create = Button(createDatasetFrame, text="CREATE", command=create)
    button_create.pack()
    button_create = Button(createDatasetFrame, text="DELETE ALL", command=deleteAll)
    button_create.pack()
    go_to_menu = Button(createDatasetFrame, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return createDatasetFrame



def createMenuFrameAlt():
    def goToCreateDatasetFrame():
        frame_menu.pack_forget()
        frame_create_dataset.pack()
        return
    def goToFrame1():
        frame_menu.pack_forget()
        frame1.pack()
        return
    def goToFrame2():
        frame_menu.pack_forget()
        frame2.pack()
        return
    def goToFrame3():
        frame_menu.pack_forget()
        frame3.pack()
        return
    def goToFrame4():
        frame_menu.pack_forget()
        frame4.pack()
        return
    def goToFrame5():
        frame_menu.pack_forget()
        frame5.pack()
        return
    def goToFrame9():
        frame_menu.pack_forget()
        frame9.pack()
        return
    def goToFrame10():
        frame_menu.pack_forget()
        frame10.pack()

    frame_menu = Frame(global_var.root_window, height = 1200, width = 1200, bg="white", padx=400)
    label_menu = Label(frame_menu, text="MENU", font="Arial 30", background="white", pady=40)
    label_menu.place(x=-70, y=0)



    #left
    label_new_1 = Label(frame_menu, text="MANAGEMENT", font="Arial 20", background="white", pady=30)
    label_new_1.place(x=-363, y=100)

    button_frame_create_pop = Button(frame_menu, text="Create random dataset", background = "#0AFAE8", command=goToCreateDatasetFrame, pady=15, width=35) #padx=40
    button_frame_create_pop.place(x=-391, y=170)



    #QUERIES
    label_new_2 = Label(frame_menu, text="QUERIES", font="Arial 20", background="white", pady=30)
    label_new_2.place(x=-70, y=100)

    button_frame1 = Button(frame_menu, text="QUERY 1\nFRAME 1", background="#FACB0A", command=goToFrame1, pady=15, width=35)
    button_frame1.place(x=-129, y=170)

    button_frame3 = Button(frame_menu, text="QUERY 3\nFRAME 3", background="#FA860A", command=goToFrame3, pady=15, width=35)
    button_frame3.place(x=-129, y=310)

    button_frame4 = Button(frame_menu, text="QUERY 4\nFRAME 4", background="#FA700A", command=goToFrame4, pady=15, width=35)
    button_frame4.place(x=-129, y=380)

    button_frame5 = Button(frame_menu, text="QUERY 5\nFRAME 5", background="#FA4B0A", command=goToFrame5, pady=15, width=35)
    button_frame5.place(x=-129, y=450)


    #COMMANDS
    label_new_3 = Label(frame_menu, text="COMMANDS", font="Arial 20", background="white", pady=30)
    label_new_3.place(x=177, y=100)

    button_frame2 = Button(frame_menu, text="COMMAND 1\nFRAME 2", background="#CE0AFA", command=goToFrame2, pady=15, width=35)
    button_frame2.place(x=134, y=170)

    button_frame9 = Button(frame_menu, text="COMMAND 3\nFRAME 9", background="#890AFA", command=goToFrame9, pady=15, width=35)
    button_frame9.place(x=134, y=310)

    button_frame10 = Button(frame_menu, text="COMMAND 4\nFRAME 10", background="#650AFA", command=goToFrame10, pady=15, width=35)
    button_frame10.place(x=134, y=380)


    button_quit = Button(frame_menu, text="QUIT", background="#FA0027", command=quit, pady=15, width=35)
    button_quit.place(x = -130, y=600)

    return frame_menu






if __name__ == "__main__":

    global_var = GlobalVariables(db = Any, root_window=createRootWindow())
    frame_login = createLoginFrame()
    frame_login.pack()
    frame_menu = createMenuFrameAlt()
    frame_create_dataset = createDatasetFrame()
    frame1 = createFrame1()
    frame2 = createFrame2()
    frame3 = createFrame3()
    frame4 = createFrame4()
    frame5 = createFrame5()
    frame9 = createFrame9()
    frame10 = createFrame10()

    global_var.root_window.mainloop()