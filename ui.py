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
import credentials_db as c_db
import qrcode as qr
import numpy as np
import functions as func



@dataclass
class GlobalVariables:
    #database
    db : pymongo.database.Database

    #ui
    root_window : Tk



def connectDbAndReturnDb(string_mongodb, db_name):
    cluster = pymongo.MongoClient(string_mongodb, tlsInsecure=True)
    db = cluster[db_name]
    db.list_collection_names()

    return db




def createLoginFrame():

    def loginAndChangeFrame():
        try:
            global_var.db = connectDbAndReturnDb(insert_string.get(), insert_db_name.get())
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

    label_string = Label(frame_login, text="Insert the string of the db:", font='Arial 30', foreground="green", background="white", pady=20)
    label_string.pack()
    insert_string = Entry(frame_login, font="Arial 8", width=100)
    insert_string.insert(0, c_db.string_mongodb)
    insert_string.pack(pady=20)

    label_name = Label(frame_login, text="Insert the string of the db:", font='Arial 30', foreground="green", background="white", pady=20)
    label_name.pack()
    insert_db_name = Entry(frame_login, font="Arial 8", width=100)
    insert_db_name.insert(0, c_db.db_name)
    insert_db_name.pack(pady=20)

    button_login = Button(frame_login, text="Login", command=loginAndChangeFrame, pady=15, padx=55)
    button_login.pack()

    button_quit = Button(frame_login, text="Quit", background= 'yellow', command=quit, pady=15, padx=58)
    button_quit.pack()

    return frame_login


def createRootWindow():
    root = Tk()
    root.title("CERTIFICATE DATABASE")
    root.geometry("900x900")
    root.configure(background="white")
    titolo = Label(root, text="SMBUD DELIVERY 2: MONGODB",font="Arial 30" ,background="white")
    titolo.pack()
    sottotitolo = Label(root, text="Giuseppe Urso, Simone Reale, Hazem Shalby, Marco Somaschini, Andrea Vitobello", font="Times 15" ,background="white", foreground="green")
    sottotitolo.pack()
    return root




#frame reale
def createFrame1():
    def goToMenu():
        sub_frame_insert.pack()

        for widget in sub_frame_qr.winfo_children():
            widget.destroy()
        label_frame1.configure(text= "GET GREEN PASS", foreground='green')
        sub_frame_qr.pack_forget()
        frame1.pack_forget()
        frame_menu.pack()
        return

    def searchGreenPass():
        col_cert = global_var.db['Certificate_Collection']
        person_name = insert_name.get().upper()
        person_surname = insert_surname.get().upper()

        query = { "name": person_name, "surname" : person_surname}
        dict_person = col_cert.find_one(query)
        validity_string = "Date expiration: " +str(func.returnCertificateExpirationDate(dict_person)) if func.returnCertificateExpirationDate(dict_person) != None else "Invalid certificate"
        label_frame1.configure(text= validity_string, foreground='red')
        label_person = Label(sub_frame_qr, text = person_name +" " +person_surname, font="Arial 20", background="white", pady=20)
        label_person.pack()

        if type(dict_person) is not type(None): 
            string_person = ""
            
            for key in dict_person:
                if key != 'list_of_vaccinations' and key != 'list_of_tests' and key != '_id':
                    string_person = string_person + str(key) +" : " +str(dict_person[key]) +"                                                        "
                
            
            img=qr.make(string_person)
            img = img.resize((600, 600), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            panel = Label(sub_frame_qr, image=img, background='white')
            panel.image = img
            panel.pack()

            

        else:

            label_person.configure(text= person_name +" " +person_surname +" NOT FOUND", font="Arial 20", foreground='red')


        sub_frame_insert.pack_forget()
        sub_frame_qr.pack()

        return


    frame1 = Frame(global_var.root_window, bg="white")
    label_frame1 = Label(frame1, text="GET GREEN PASS", font="Arial 25", background="white", foreground='green' ,pady=10)
    label_frame1.pack()

    sub_frame_qr = Frame(frame1, bg='white')
    sub_frame_insert = Frame(frame1, bg = 'white')
    sub_frame_insert.pack()
    

    #name
    Label(sub_frame_insert, text="Insert the name of patient:", font='Arial 15', foreground="green",background="white", pady=5).pack()
    insert_name = Entry(sub_frame_insert, font="Arial 20")
    insert_name.pack(pady=5)
    #surname
    Label(sub_frame_insert, text="Insert the surname of patient:", font='Arial 15', foreground="green",background="white", pady=5).pack()
    insert_surname = Entry(sub_frame_insert, font="Arial 20")
    insert_surname.pack(pady=5)

    #add button
    button_search = Button(sub_frame_insert, text="FIND GREEN PASS!", command=searchGreenPass, padx=30, pady=30)
    button_search.pack()

    go_to_menu = Button(frame1, text="Go to Menu", command=goToMenu, padx=30, pady=30)
    go_to_menu.pack()
    return frame1




#frame comando aggiungi vaccino Reale
def createFrame2():
    def goToMenu():
        label_frame2.configure(text="ADD A VACCINE", foreground="black") 
        frame2.pack_forget()
        frame_menu.pack()
        return

    #da trovare un modo per fare tutto con una query soltanto
    def addVaccine():
        col_cert = global_var.db['Certificate_Collection']
        person_name = insert_name.get().upper()
        person_surname = insert_surname.get().upper()   
        query = { "name": person_name, "surname" : person_surname}
        dict_person = col_cert.find_one(query)
        
        if type(dict_person) is not type(None):
            label_frame2.configure(text="ADD A VACCINE", foreground='black') 
            list_of_vaccinations = dict_person['list_of_vaccinations']
            try:
                lotto = int(insert_lot.get())
            except:
                 label_frame2.configure(text="LOT IS A NUMBER!", foreground="red")
                 return

            new_vaccine= func.createVaccine(option_vaccine_brand_variable.get(), lotto, str(cal_date.get_date()), 
                                            str(cal_production.get_date()), insert_location.get(), insert_cf_doctor.get().upper())

            list_of_vaccinations.append(new_vaccine)
            newvalues = { "$set": { "list_of_vaccinations": list_of_vaccinations } }
            col_cert.update_one(query, newvalues)


            #aggiorno la validità
            func.updateValidity(col_cert, person_name, person_surname)

        else:
            label_frame2.configure(text="ERROR", foreground="red")


  
    frame2 = Frame(global_var.root_window, bg="white")
    label_frame2 = Label(frame2, text="ADD A VACCINE", font="Arial 30", background="white", pady=10)
    label_frame2.grid(row=15, column=0)

    left_frame = Frame(frame2, background='white')
    left_frame.grid(row=0, column=0, sticky="nswe")

    right_frame = Frame(frame2, background='white')
    right_frame.grid(row=0, column=1, sticky="nswe")

    #name
    Label(left_frame, text="Insert the name of the patient:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=0, column=0, sticky="nswe")
    insert_name = Entry(left_frame, font="Arial 10")
    insert_name.grid(row=1, column=0, sticky="nswe")
    #surname
    Label(left_frame, text="Insert the surname of the patient:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=2, column=0, sticky="nswe")
    insert_surname = Entry(left_frame, font="Arial 10")
    insert_surname.grid(row=3, column=0, sticky="nswe")
    #brand
    choices = conf.vaccines
    option_vaccine_brand_variable = StringVar(left_frame)
    option_vaccine_brand_variable.set(conf.vaccines[0])
    Label(left_frame, text="Choose the brand::", font='Arial 10', foreground="green",background="white", pady=5).grid(row=4, column=0, sticky="nswe")
    option_test_type = OptionMenu(left_frame, option_vaccine_brand_variable, *choices)
    option_test_type.grid(row=5, column=0, sticky="nswe")
    #test date
    Label(right_frame, text="Insert vaccine date:", font='Arial 10', foreground="green", background="white", pady=5).grid(row=0, column=0, sticky="nswe")
    cal_date= Calendar(right_frame, date_pattern="yyyy-mm-dd")
    cal_date.grid(row=1, column=0, sticky="nswe")
    #production date
    Label(right_frame, text="Insert date of production:", font='Arial 10', foreground="green", background="white", pady=5).grid(row=2, column=0, sticky="nswe")
    cal_production= Calendar(right_frame, date_pattern="yyyy-mm-dd")
    cal_production.grid(row=3, column=0, sticky="nswe")
    #lot
    Label(left_frame, text="Insert the lot of the vaccine (it's a number):", font='Arial 10', foreground="green",background="white", pady=5).grid(row=6, column=0, sticky="nswe")
    insert_lot = Entry(left_frame, font="Arial 10")
    insert_lot.grid(row=7, column=0, sticky="nswe")
    #location
    Label(left_frame, text="Insert the location:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=8, column=0, sticky="nswe")
    insert_location = Entry(left_frame, font="Arial 10")
    insert_location.grid(row=9, column=0, sticky="nswe")
    #cf_doctor
    Label(left_frame, text="Insert the name and the surname of the doctor:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=10, column=0, sticky="nswe")
    insert_cf_doctor = Entry(left_frame, font="Arial 10")
    insert_cf_doctor.grid(row=11, column=0, sticky="nswe")

    #add button
    button_search = Button(left_frame, text="Add Vaccine!", command=addVaccine, padx=30, pady=30)
    button_search.grid(row=12, column=0, sticky="nswe")

    go_to_menu = Button(left_frame, text="Go to Menu", command=goToMenu)
    go_to_menu.grid(row=13, column=0, sticky="nswe")
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
        tree.pack_forget()
        frame_menu.pack()
        return
    def searchVaccines():
        for row in tree.get_children():
            tree.delete(row)

        tree.pack_forget()
        tree.pack()
        tree.heading(1, text="Brand")
        tree.heading(2, text="Lot")
        tree.heading(3, text="Date")
        tree.heading(4, text="Prod. date")
        tree.heading(5, text="Location")
        tree.heading(6, text="CF Doctor")

        tree.column(1, width=120)
        tree.column(2, width=120)
        tree.column(3, width=120)
        tree.column(4, width=120)
        tree.column(5, width=120)
        tree.column(6, width=120)

        col_cert = global_var.db['Certificate_Collection']
        person_name = insert_name.get().upper()
        person_surname = insert_surname.get().upper()

        query = {"name": person_name, "surname": person_surname}
        dict_person = col_cert.find_one(query)

        #if type(dict_person) is not type(None):
        #    for vaccination in dict_person['list_of_vaccinations']:
        #        for key in vaccination:
        #            print(key)
        #            print(vaccination[key])
        if type(dict_person) is not type(None):
            for vaccination in dict_person['list_of_vaccinations']:
                tree.insert('', 'end', values=(vaccination['brand'], vaccination['lot'], vaccination['date'], vaccination['production_date'], vaccination['location'], vaccination['cf_doctor']))
        return
    def searchTests():
        for row in tree.get_children():
            tree.delete(row)

        tree.pack_forget()
        tree.pack()
        tree.heading(1, text="Test type")
        tree.heading(2, text="Date")
        tree.heading(3, text="Location")
        tree.heading(4, text="Result")
        tree.heading(5, text="CF Doctor")
        tree.heading(6, text="")

        tree.column(1, width=120)
        tree.column(2, width=120)
        tree.column(3, width=120)
        tree.column(4, width=120)
        tree.column(5, width=120)
        tree.column(6, width=0)

        col_cert = global_var.db['Certificate_Collection']
        person_name = insert_name.get().upper()
        person_surname = insert_surname.get().upper()

        query = {"name": person_name, "surname": person_surname}
        dict_person = col_cert.find_one(query)

        # if type(dict_person) is not type(None):
        #    for vaccination in dict_person['list_of_vaccinations']:
        #        for key in vaccination:
        #            print(key)
        #            print(vaccination[key])
        if type(dict_person) is not type(None):
            for test in dict_person['list_of_tests']:
                tree.insert('', 'end', values=(
                test['test_type'], test['date'], test['location'], test['result'],
                test['cf_doctor']))
        return

    frame4 = Frame(global_var.root_window, bg="white")
    label_frame4 = Label(frame4, text="FRAME 4 URSO", font="20", background="white", pady=5)
    label_frame4.pack()

    sub_frame_qr = Frame(frame4, bg='white')
    sub_frame_insert = Frame(frame4, bg='white')
    sub_frame_insert.pack()

    # name
    Label(sub_frame_insert, text="Insert the name of patient:", font='Arial 15', foreground="green", background="white",
          pady=2).pack()
    insert_name = Entry(sub_frame_insert, font="Arial 20")
    insert_name.pack(pady=2)
    # surname
    Label(sub_frame_insert, text="Insert the surname of patient:", font='Arial 15', foreground="green",
          background="white", pady=5).pack()
    insert_surname = Entry(sub_frame_insert, font="Arial 20")
    insert_surname.pack(pady=2)

    # add button
    button_search_vaccines = Button(sub_frame_insert, text="FIND VACCINES!", command=searchVaccines, padx=30, pady=10)
    button_search_vaccines.pack()

    button_search_tests = Button(sub_frame_insert, text="FIND TESTS!", command=searchTests, padx=30, pady=10)
    button_search_tests.pack()

    tree = Treeview(frame4, columns = (1,2,3,4,5,6), height = 10, show = "headings")

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




#frame add test
def createFrame9():
    def goToMenu():
        label_frame9.configure(text="ADD A TEST")
        frame9.pack_forget()
        frame_menu.pack()
        return

    #da trovare un modo per fare tutto con una query soltanto
    def addTest():
        col_cert = global_var.db['Certificate_Collection']
        person_name = insert_name.get().upper()
        person_surname = insert_surname.get().upper()   
        query = { "name": person_name, "surname" : person_surname}
        dict_person = col_cert.find_one(query)
        if type(dict_person) is not type(None):
            label_frame9.configure(text="ADD A TEST")
            list_of_tests = dict_person['list_of_tests']

            result = False if test_result.get() == 0 else True

            new_test= func.createTest(option_test_type_variable.get(), str(cal_date.get_date()), 
                                    insert_location.get(), result, insert_cf_doctor.get().upper())

            list_of_tests.append(new_test)
            newvalues = { "$set": { "list_of_tests": list_of_tests } }
            col_cert.update_one(query, newvalues)


            func.updateValidity(col_cert, person_name, person_surname)

        else:
            label_frame9.configure(text="ERROR")
        


  
    frame9 = Frame(global_var.root_window, bg="white")
    label_frame9 = Label(frame9, text="ADD A TEST", font="Arial 30", background="white", pady=10)
    label_frame9.grid(row=16, column=0)

    left_frame = Frame(frame9, background='white')
    left_frame.grid(row=0, column=0, sticky="nswe")

    right_frame = Frame(frame9, background='white')
    right_frame.grid(row=0, column=1, sticky="nswe")

    test_result = IntVar()

    #name
    Label(left_frame, text="Insert the name of the patient:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=0, column=0, sticky="nswe")
    insert_name = Entry(left_frame, font="Arial 10")
    insert_name.grid(row=1, column=0, sticky="nswe")
    #surname
    Label(left_frame, text="Insert the surname of the patient:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=2, column=0, sticky="nswe")
    insert_surname = Entry(left_frame, font="Arial 10")
    insert_surname.grid(row=3, column=0, sticky="nswe")
    #test type
    choices = conf.type_of_test
    option_test_type_variable = StringVar(left_frame)
    option_test_type_variable.set(conf.type_of_test[0])
    Label(left_frame, text="Choose the type of the test:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=4, column=0, sticky="nswe")
    option_test_type = OptionMenu(left_frame, option_test_type_variable, *choices)
    option_test_type.grid(row=5, column=0, sticky="nswe")
    #test date
    Label(right_frame, text="Insert test date:", font='Arial 10', foreground="green", background="white", pady=5).grid(row=0, column=0, sticky="nswe")
    cal_date= Calendar(right_frame, date_pattern="yyyy-mm-dd")
    cal_date.grid(row=1, column=0, sticky="nswe")
    #location
    Label(left_frame, text="Insert the location:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=6, column=0, sticky="nswe")
    insert_location = Entry(left_frame, font="Arial 10")
    insert_location.grid(row=7, column=0, sticky="nswe")
    #test result
    ChkBttn = Checkbutton(left_frame, variable=test_result, text="Tick if the result is positive", font="Arial 15" ,background="white")
    ChkBttn.grid(row=10, column=0, sticky="nswe")
    #cf_doctor
    Label(left_frame, text="Insert the name and the surname of the doctor:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=11, column=0, sticky="nswe")
    insert_cf_doctor = Entry(left_frame, font="Arial 10")
    insert_cf_doctor.grid(row=12, column=0, sticky="nswe")

    #add button
    button_search = Button(left_frame, text="Add Test!", command=addTest, padx=30, pady=30)
    button_search.grid(row=13, column=0, sticky="nswe")

    go_to_menu = Button(left_frame, text="Go to Menu", command=goToMenu)
    go_to_menu.grid(row=14, column=0, sticky="nswe")
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
    label_createpopframe = Label(createDatasetFrame, text="CREATE DATASET: NUMBER OF PEOPLE", font="Arial 30", foreground="green" ,background="white", pady=20)
    label_createpopframe.pack()
    scale_pop = Scale(createDatasetFrame, from_=10, to=800, orient="horizontal", background="white", length=400, cursor="plus", font="Arial 30")
    scale_pop.set(400)
    scale_pop.pack(pady=15)
    button_create = Button(createDatasetFrame, text="CREATE", command=create, padx=40, pady=40)
    button_create.pack(padx=30, pady=30)
    button_create = Button(createDatasetFrame, text="DELETE ALL", background="red" ,command=deleteAll, padx=30, pady=30)
    button_create.pack(padx= 5, pady = 10)
    go_to_menu = Button(createDatasetFrame, text="Go to Menu", command=goToMenu, padx=30, pady=30)
    go_to_menu.pack(padx= 5, pady = 10)
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

    button_frame1 = Button(frame_menu, text="QUERY 1\nGET GREEN PASS 1", background="#FACB0A", command=goToFrame1, pady=15, width=35)
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

    button_frame2 = Button(frame_menu, text="COMMAND 1\nADD A VACCINE", background="#CE0AFA", command=goToFrame2, pady=15, width=35)
    button_frame2.place(x=134, y=170)

    button_frame9 = Button(frame_menu, text="COMMAND 3\nADD A TEST", background="#890AFA", command=goToFrame9, pady=15, width=35)
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