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
import pprint



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

    img = Image.open('images\\green_pass.jpg')
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

    label_name = Label(frame_login, text="Insert the name of the db:", font='Arial 30', foreground="green", background="white", pady=20)
    label_name.pack()
    insert_db_name = Entry(frame_login, font="Arial 20", width=30)
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
        person_cf = insert_cf.get().upper()

        query = { "cf": person_cf}
        dict_person = col_cert.find_one(query)
        validity_string = "Date expiration: " +str(func.returnCertificateExpirationDate(dict_person)) if func.returnCertificateExpirationDate(dict_person) != None else "Invalid certificate"
        label_frame1.configure(text= validity_string, foreground='red')
        label_person = Label(sub_frame_qr, text = dict_person['name'] +" " +dict_person['surname'], font="Arial 20", background="white", pady=20)
        label_person.pack()

        if type(dict_person) is not type(None): 
            string_person = ""
            
            for key in dict_person:
                if key != 'list_of_vaccinations' and key != 'list_of_tests' and key != '_id':
                    string_person = string_person + str(key) +" : " +str(dict_person[key]) +"                                                        "
                
            
        

            
            qr_class = qr.QRCode(
                                version=1,
                                error_correction=qr.constants.ERROR_CORRECT_L,
                                box_size=10,
                                border=1,
                                )
            qr_class.add_data(string_person)
            qr_class.make(fit=True)

            img = qr_class.make_image(fill_color="white", back_color="black")


            img = img.resize((500, 500), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            panel = Label(sub_frame_qr, image=img, background='white')
            panel.image = img
            panel.pack()

            

        else:

            label_person.configure(text = dict_person['name'] +" " +dict_person['surname'] +" NOT FOUND", font="Arial 20", foreground='red')


        sub_frame_insert.pack_forget()
        sub_frame_qr.pack()

        return


    frame1 = Frame(global_var.root_window, bg="white")
    label_frame1 = Label(frame1, text="GET GREEN PASS", font="Arial 25", background="white", foreground='green' ,pady=10)
    label_frame1.pack()

    sub_frame_qr = Frame(frame1, bg='white')
    sub_frame_insert = Frame(frame1, bg = 'white')
    sub_frame_insert.pack()
    

    #cf
    Label(sub_frame_insert, text="Insert the cf of the patient:", font='Arial 15', foreground="green",background="white", pady=5).pack()
    insert_cf = Entry(sub_frame_insert, font="Arial 20")
    insert_cf.pack(pady=5)

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
        person_cf = insert_cf.get().upper()
        query = { "cf": person_cf}
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
                                            str(cal_production.get_date()), insert_location.get(), insert_cf_doctor.get().upper(), int(insert_piva.get()))

            list_of_vaccinations.append(new_vaccine)
            newvalues = { "$set": { "list_of_vaccinations": list_of_vaccinations } }
            col_cert.update_one(query, newvalues)


            #aggiorno la validità
            func.updateValidity(col_cert, person_cf)

        else:
            label_frame2.configure(text="ERROR", foreground="red")


  
    frame2 = Frame(global_var.root_window, bg="white")
    label_frame2 = Label(frame2, text="ADD A VACCINE", font="Arial 30", background="white", pady=10)
    label_frame2.grid(row=15, column=0)

    left_frame = Frame(frame2, background='white')
    left_frame.grid(row=0, column=0, sticky="nswe")

    right_frame = Frame(frame2, background='white')
    right_frame.grid(row=0, column=1, sticky="nswe")

    #cf
    Label(left_frame, text="Insert the cf of the patient:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=0, column=0, sticky="nswe")
    insert_cf = Entry(left_frame, font="Arial 10")
    insert_cf.grid(row=1, column=0, sticky="nswe")
    #piva
    Label(left_frame, text="Insert the piva of the authorized body:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=2, column=0, sticky="nswe")
    insert_piva = Entry(left_frame, font="Arial 10")
    insert_piva.grid(row=3, column=0, sticky="nswe")
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
    def getLocationWithMostVaccines():
        for row in treeVax.get_children():
            treeVax.delete(row)

        treeVax.pack_forget()
        treeVax.pack(padx=30, pady=10)
        treeVax.heading(1, text="Type")
        treeVax.heading(2, text="PIVA")
        treeVax.heading(3, text="# of vaccines")

        treeVax.column(1, width=120)
        treeVax.column(2, width=120)
        treeVax.column(3, width=120)

        for line in func.getLocationWithMostVaccines(global_var.db['Certificate_Collection'], global_var.db['AuthorizedBodies_Collection']):
            treeVax.insert('', 'end', values=(line['Type'], line['PIVA'], line['NofVax']))

        return 

    def getLocationWithMostTest():
        for row in treeTest.get_children():
            treeTest.delete(row)

        treeTest.pack_forget()
        treeTest.pack(padx=30, pady=10)
        treeTest.heading(1, text="Type")
        treeTest.heading(2, text="PIVA")
        treeTest.heading(3, text="# of tests")

        treeTest.column(1, width=120)
        treeTest.column(2, width=120)
        treeTest.column(3, width=120)

        for line in func.getLocationWithMostTests(global_var.db['Certificate_Collection'], global_var.db['AuthorizedBodies_Collection']):
            treeTest.insert('', 'end', values=(line['Type'], line['PIVA'], line['NofTest']))

        return

    def getLocations():
        getLocationWithMostVaccines()
        getLocationWithMostTest()
    

    def goToMenu():
        frame3.pack_forget()
        frame_menu.pack()
        return

    frame3 = Frame(global_var.root_window, bg="white")
    label_frame3 = Label(frame3, text="QUERY 3: LOCATIONS WITH MOST VACCINES/TESTS", font="20", background="white", pady=20)
    label_frame3.pack()

    button_create = Button(frame3, text="Find", command=getLocations, padx=20, pady=10)
    button_create.pack(padx=30, pady=10)

    treeVax = Treeview(frame3, columns = (1,2,3), height = 3, show = "headings")
    treeTest = Treeview(frame3, columns = (1,2,3), height = 3, show = "headings")

    go_to_menu = Button(frame3, text="Go to Menu", command=goToMenu)
    go_to_menu.pack(padx=30, pady=10)
    
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
        tree.pack_forget()
        return

    def getInput():
        for row in tree.get_children():
            tree.delete(row)

        tree.pack_forget()
        tree.pack()
        tree.heading(1, text="Name")
        tree.heading(2, text="Surname")
        tree.heading(3, text="Birth Date")
        tree.heading(4, text="CF")
        tree.column(1, width = 100)
        tree.column(2, width = 100)
        tree.column(3, width = 100)
        tree.column(4, width = 100)

        col_cert = global_var.db['Certificate_Collection']
        lot = insert_lot.get()
        query = {"list_of_vaccinations" : { "$elemMatch" : { "lot" :  int(lot)  }}}
        dict_person = col_cert.find(query)

        if type(dict_person) is not type(None):
            for person in dict_person:
                tree.insert('', 'end', values=(person['name'], person['surname'], person['birthdate'], person['cf'] ))
        return

    frame5 = Frame(global_var.root_window, bg="white")
    label_frame5 = Label(frame5, text="FIND PEOPLE WHO WERE VACCINATED WITH LOT", font="20", background="white", pady=20)
    label_frame5.pack()

    #sub_frame_qr = Frame(frame5, bg='white')
    sub_frame_insert = Frame(frame5, bg='white')
    sub_frame_insert.pack()
    Label(sub_frame_insert, text="Insert the lot value (7 int values):", font='Arial 15', foreground="green", background="white", pady=2).pack()
    insert_lot = Entry(sub_frame_insert, font="Arial 20")
    insert_lot.pack(pady=2)    
    button_search = Button(sub_frame_insert, text="FIND PEOPLE!", command=getInput, padx=30, pady=10)
    button_search.pack()

    tree = Treeview(frame5, columns = (1,2,3,4), height = 10, show = "headings")

    go_to_menu = Button(frame5, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()

    return frame5


def createFrame6():
    [data, labels] = func.getNumOfVaccinePerPerson(global_var.db['Certificate_Collection'])
    # [data, labels] = functions.getInfectedPerPlaceType(global_var.db_graph)

    # Wedge properties
    wp = {'linewidth': 1, 'edgecolor': "green"}

    # Creating autocpt arguments
    def function(pct, allvalues):
        absolute = int(pct / 100. * np.sum(allvalues))
        return "{:.1f}%\n({:d} p)".format(pct, absolute)

    # Creating plot
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(data,
                                      autopct=lambda pct: function(pct, data),
                                      labels=labels,
                                      wedgeprops=wp,
                                      textprops=dict(color="magenta"))

    # Adding legend
    ax.legend(wedges, labels,
              title="#doses executed",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title("vaccine doses executed for each person")

    # show plot
    plt.show()

    return

#get pie chart with numers of tests for each person
def createFrame7():
        [data, labels] =func.getNumOfTestPerPerson( global_var.db['Certificate_Collection'])
        #[data, labels] = functions.getInfectedPerPlaceType(global_var.db_graph)

        # Wedge properties
        wp = {'linewidth': 1, 'edgecolor': "green"}

        # Creating autocpt arguments
        def function(pct, allvalues):
            absolute = int(pct / 100. * np.sum(allvalues))
            return "{:.1f}%\n({:d} p)".format(pct, absolute)

        # Creating plot
        fig, ax = plt.subplots(figsize=(10, 7))
        wedges, texts, autotexts = ax.pie(data,
                                          autopct=lambda pct: function(pct, data),
                                          labels=labels,
                                          wedgeprops=wp,
                                          textprops=dict(color="magenta"))

        # Adding legend
        ax.legend(wedges, labels,
                  title="#tests executed",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title("test executed for each person")

        # show plot
        plt.show()

        return


def createFrame8():
    [data, labels] = func.getNumOfDosesPerVaccine(global_var.db['Certificate_Collection'])
    # [data, labels] = functions.getInfectedPerPlaceType(global_var.db_graph)

    # Wedge properties
    wp = {'linewidth': 1, 'edgecolor': "green"}

    # Creating autocpt arguments
    def function(pct, allvalues):
        absolute = int(pct / 100. * np.sum(allvalues))
        return "{:.1f}%\n({:d} d)".format(pct, absolute)

    # Creating plot
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(data,
                                      autopct=lambda pct: function(pct, data),
                                      labels=labels,
                                      wedgeprops=wp,
                                      textprops=dict(color="magenta"))

    # Adding legend
    ax.legend(wedges, labels,
              title="vaccine type",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title("number of dosese per vaccine")

    # show plot
    plt.show()

    return


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
        person_cf = insert_cf.get().upper()  
        query = { "cf": person_cf}
        dict_person = col_cert.find_one(query)
        if type(dict_person) is not type(None):
            label_frame9.configure(text="ADD A TEST")
            list_of_tests = dict_person['list_of_tests']

            result = False if test_result.get() == 0 else True

            new_test= func.createTest(option_test_type_variable.get(), str(cal_date.get_date()), 
                                    insert_location.get(), result, insert_cf_doctor.get().upper(), int(insert_piva.get()))

            list_of_tests.append(new_test)
            newvalues = { "$set": { "list_of_tests": list_of_tests } }
            col_cert.update_one(query, newvalues)


            func.updateValidity(col_cert, person_cf)

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
    Label(left_frame, text="Insert the cf of the patient:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=0, column=0, sticky="nswe")
    insert_cf = Entry(left_frame, font="Arial 10")
    insert_cf.grid(row=1, column=0, sticky="nswe")
    #piva
    Label(left_frame, text="Insert the piva of the authorized body:", font='Arial 10', foreground="green",background="white", pady=5).grid(row=2, column=0, sticky="nswe")
    insert_piva = Entry(left_frame, font="Arial 10")
    insert_piva.grid(row=3, column=0, sticky="nswe")
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

    def updateAuthBody():
        col_authBody = global_var.db['AuthorizedBodies_Collection']
        PIVA=insert_name.get()
        description=insert_description.get().lower() + "\n"
        if insert_active.get().lower() == "true" or insert_active.get().lower() == "false":
            if insert_active.get().lower() == "true" :
                active = True
            if insert_active.get().lower() == "false" :
                active = False
            filter = { "piva" : int(PIVA)}
            values = [{ "$set" : { "active" : active, "description" :  {"$concat": [ {"$ifNull" : ["$description", ""]}, description ]} }}]

        else:
            filter = {"piva" : int(PIVA)}
            values = [{ "$set" : { "description" :  {"$concat": [ {"$ifNull" : ["$description", ""]}, description ]}}}]
        col_authBody.update_one(filter, values)

    frame10 = Frame(global_var.root_window, bg="white")
    label_frame10 = Label(frame10, text="UPDATE STATE OF AUTHORIZED BODY", font="Arial 30", background="white", pady=10)
    label_frame10.grid(row=15, column=0)

    left_frame = Frame(frame10, background='white')
    left_frame.grid(row=0, column=0, sticky="nswe")

    right_frame = Frame(frame10, background='white')
    right_frame.grid(row=0, column=1, sticky="nswe")

    # name
    Label(left_frame, text="Select the PIVA of the auth. body to update:", font='Arial 10', foreground="green", background="white",
          pady=5).grid(row=0, column=0, sticky="nswe")
    insert_name = Entry(left_frame, font="Arial 10")
    insert_name.grid(row=1, column=0, sticky="nswe")
    # description
    Label(left_frame, text="Insert the description TO CONCAT:", font='Arial 10', foreground="green",
          background="white", pady=5).grid(row=8, column=0, sticky="nswe")
    insert_description = Entry(left_frame, font="Arial 10")
    insert_description.grid(row=9, column=0, sticky="nswe")
    # active
    Label(left_frame, text="is the body active?(true/false, not mandatory):", font='Arial 10', foreground="green",
          background="white", pady=5).grid(row=12, column=0, sticky="nswe")
    insert_active = Entry(left_frame, font="Arial 10")
    insert_active.grid(row=13, column=0, sticky="nswe")
    # add button
    button_search = Button(left_frame, text="Update Authorized Body!", command=updateAuthBody, padx=30, pady=30)
    button_search.grid(row=16, column=0, sticky="nswe")

    go_to_menu = Button(left_frame, text="Go to Menu", command=goToMenu)
    go_to_menu.grid(row=17, column=0, sticky="nswe")
    return frame10


def createFrame11():
    def goToMenu():
        label_frame11.configure(text="ADD AN AUTHORIZED BODY", foreground="black")
        frame11.pack_forget()
        frame_menu.pack()
        return

    def addAuthBody():
        col_authBody = global_var.db['AuthorizedBodies_Collection']
        new_auth_body = func.createGoodAuthorizedBody(name=insert_name.get(), piva= int(insert_piva.get()), type=insert_type.get(),
                                                          address=insert_addr.get(), gps=insert_location.get(), department=insert_dept.get(),
                                                          description=insert_description.get(), doctors=insert_docs.get())
        col_authBody.insert_one(new_auth_body)

    frame11 = Frame(global_var.root_window, bg="white")
    label_frame11 = Label(frame11, text="ADD AN AUTHORIZED BODY", font="Arial 30", background="white", pady=10)
    label_frame11.grid(row=15, column=0)

    left_frame = Frame(frame11, background='white')
    left_frame.grid(row=0, column=0, sticky="nswe")

    right_frame = Frame(frame11, background='white')
    right_frame.grid(row=0, column=1, sticky="nswe")

    # name
    Label(left_frame, text="Insert the name of the auth. body:", font='Arial 10', foreground="green", background="white",
          pady=5).grid(row=0, column=0, sticky="nswe")
    insert_name = Entry(left_frame, font="Arial 10")
    insert_name.grid(row=1, column=0, sticky="nswe")
    # piva
    Label(left_frame, text="Insert the 'partita IVA':", font='Arial 10', foreground="green",
          background="white", pady=5).grid(row=2, column=0, sticky="nswe")
    insert_piva = Entry(left_frame, font="Arial 10")
    insert_piva.grid(row=3, column=0, sticky="nswe")
    # type
    Label(left_frame, text="Insert the type of entity:", font='Arial 10', foreground="green",
          background="white", pady=5).grid(row=4, column=0, sticky="nswe")
    insert_type = Entry(left_frame, font="Arial 10")
    insert_type.grid(row=5, column=0, sticky="nswe")
    # address
    Label(left_frame, text="Insert the address:", font='Arial 10', foreground="green",
          background="white", pady=5).grid(row=6, column=0, sticky="nswe")
    insert_addr = Entry(left_frame, font="Arial 10")
    insert_addr.grid(row=7, column=0, sticky="nswe")
    # location
    Label(left_frame, text="Insert the location (GPS):", font='Arial 10', foreground="green", background="white",
          pady=5).grid(row=8, column=0, sticky="nswe")
    insert_location = Entry(left_frame, font="Arial 10")
    insert_location.grid(row=9, column=0, sticky="nswe")
    # department
    Label(left_frame, text="Insert the department issuing vaccine:", font='Arial 10', foreground="green",
          background="white", pady=5).grid(row=10, column=0, sticky="nswe")
    insert_dept = Entry(left_frame, font="Arial 10")
    insert_dept.grid(row=11, column=0, sticky="nswe")
    # description
    Label(left_frame, text="Insert the description:", font='Arial 10', foreground="green",
          background="white", pady=5).grid(row=12, column=0, sticky="nswe")
    insert_description = Entry(left_frame, font="Arial 10")
    insert_description.grid(row=13, column=0, sticky="nswe")
    # doctors
    Label(left_frame, text="Insert the doctors (separated by ';' charachter):", font='Arial 10', foreground="green",
          background="white", pady=5).grid(row=14, column=0, sticky="nswe")
    insert_docs = Entry(left_frame, font="Arial 10")
    insert_docs.grid(row=15, column=0, sticky="nswe")

    # add button
    button_search = Button(left_frame, text="Add Authorized Body!", command=addAuthBody, padx=30, pady=30)
    button_search.grid(row=16, column=0, sticky="nswe")

    go_to_menu = Button(left_frame, text="Go to Menu", command=goToMenu)
    go_to_menu.grid(row=17, column=0, sticky="nswe")
    return frame11

"""def createFrame11():
    def goToMenu():
        frame11.pack_forget()
        frame_menu.pack()
        return

    frame11 = Frame(global_var.root_window, bg="white")
    label_frame11 = Label(frame11, text="FRAME 11 URSO", font="20", background="white", pady=20)
    label_frame11.pack()
    go_to_menu = Button(frame11, text="Go to Menu", command=goToMenu)
    go_to_menu.pack()
    return frame11
"""

# Frame Somaschini 2
def createFrame12():
    def addPerson():
        if entries['First Name'].get() == "" or entries['Last Name'].get() == "" or entries['Birthdate'].get_date() == "" or entries['Details'].get() == "":
            log = "Some entries are missing"
        else:
            log = func.addPerson(
                    global_var.db['Certificate_Collection'],
                    entries['First Name'].get().upper(),
                    entries['Last Name'].get().upper(),
                    entries['Birthdate'].get_date(),
                    entries['Details'].get()
            )

        label_output.config(text=log)
        label_output.pack()
        return

    def goToMenu():
        frame12.pack_forget()
        label_output.pack_forget()
        frame_menu.pack()
        return

    frame12 = Frame(global_var.root_window, bg="white")
    label_frame12 = Label(frame12, text="COMMAND: ADD A PERSON", font="20", background="white", pady=20)
    label_frame12.pack()

    entries = {
        "First Name":   Entry(frame12),
        "Last Name":    Entry(frame12),
        "Birthdate":    Calendar(frame12, date_pattern="yyyy-mm-dd"),
        "Details":      Entry(frame12)
    }
    for label, entry in entries.items():
        Label(frame12, text = label).pack()
        entry.pack(pady=5)

    add_contact = Button(frame12, text="Add Contact", command=addPerson)
    add_contact.pack(pady=5)

    go_to_menu = Button(frame12, text="Go to Menu", command=goToMenu)
    go_to_menu.pack(pady=5)

    label_output = Label(frame12, text="", font='Arial 14', background="white", foreground="black")
    label_output.pack()

    return frame12


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

    def goToFrame6():
        frame_menu.pack_forget()
        frame6.pack()
        return


    def goToFrame9():
        frame_menu.pack_forget()
        frame9.pack()
        return
    def goToFrame10():
        frame_menu.pack_forget()
        frame10.pack()

    def goToFrame11():
        frame_menu.pack_forget()
        frame11.pack()

    def goToFrame12():
        frame_menu.pack_forget()
        frame12.pack()

    frame_menu = Frame(global_var.root_window, height = 1200, width = 1200, bg="white", padx=400)
    label_menu = Label(frame_menu, text="MENU", font="Arial 30", background="white", pady=40)
    label_menu.place(x=-70, y=0)



    #left
    label_new_1 = Label(frame_menu, text="MANAGEMENT", font="Arial 20", background="white", pady=30)
    label_new_1.place(x=-363, y=100)

    button_frame_create_pop = Button(frame_menu, text="CREATE/DELETE RANDOM DATASET", background = "#0AFAE8", command=goToCreateDatasetFrame, pady=15, width=35) #padx=40
    button_frame_create_pop.place(x=-391, y=170)

    button_quit = Button(frame_menu, text="QUIT", background="#FA0027", command=quit, pady=15, width=35)
    button_quit.place(x = -391, y=240)



    #QUERIES
    label_new_2 = Label(frame_menu, text="QUERIES", font="Arial 20", background="white", pady=30)
    label_new_2.place(x=-70, y=100)

    button_frame1 = Button(frame_menu, text="QUERY 1\nGET GREEN PASS 1", background="#FACB0A", command=goToFrame1, pady=15, width=35)
    button_frame1.place(x=-129, y=170)

    button_frame3 = Button(frame_menu, text="QUERY 3\nGET LOCATIONS WITH MOST VACCINES/TESTS", background="#FA860A", command=goToFrame3, pady=15, width=35)
    button_frame3.place(x=-129, y=310)

    button_frame4 = Button(frame_menu, text="QUERY 4\nSEARCH VACCINES/TESTS FOR EACH PERSON", background="#FA700A", command=goToFrame4, pady=15, width=35)
    button_frame4.place(x=-129, y=380)

    button_frame5 = Button(frame_menu, text="QUERY 5\nSEARCH PEOPLE VACCINATED WITH LOTS", background="#FA4B0A", command=goToFrame5, pady=15, width=35)
    button_frame5.place(x=-129, y=450)

    button_frame6 = Button(frame_menu, text="QUERY 6\nNUMBER OF VACCINE PER PERSON", background="#FA4B0A", command=createFrame6, pady=15, width=35)
    button_frame6.place(x=-129, y=520)

    button_frame7 = Button(frame_menu, text="QUERY 7\nNUMBER OF TEST PER PERSON", background="#FA4B0A", command=createFrame7, pady=15, width=35)
    button_frame7.place(x=-129, y=590)

    button_frame8 = Button(frame_menu, text="QUERY 8\nNUMBER OF DOSES PER VACCINE", background="#FA4B0A",command=createFrame8, pady=15, width=35)
    button_frame8.place(x=-129, y=660)


    #COMMANDS
    label_new_3 = Label(frame_menu, text="COMMANDS", font="Arial 20", background="white", pady=30)
    label_new_3.place(x=177, y=100)

    button_frame2 = Button(frame_menu, text="COMMAND 1\nADD A VACCINE", background="#CE0AFA", command=goToFrame2, pady=15, width=35)
    button_frame2.place(x=134, y=170)

    button_frame9 = Button(frame_menu, text="COMMAND 3\nADD A TEST", background="#890AFA", command=goToFrame9, pady=15, width=35)
    button_frame9.place(x=134, y=310)

    button_frame10 = Button(frame_menu, text="COMMAND 4\nUPDATE STATE OF AUTHORIZED BODY ", background="#650AFA", command=goToFrame10, pady=15, width=35)
    button_frame10.place(x=134, y=380)

    button_frame11 = Button(frame_menu, text="COMMAND 5\nADD AN AUTHORIZED BODY", background="#650AFA", command=goToFrame11, pady=15, width=35)
    button_frame11.place(x=134, y=450)

    button_frame12 = Button(frame_menu, text="COMMAND 6\nADD A PERSON", background="#650AFA", command=goToFrame12, pady=15, width=35)
    button_frame12.place(x=134, y=520)

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
    #frame6 = createFrame6()
    #frame7 = createFrame7()
    frame9 = createFrame9()
    frame10 = createFrame10()
    frame11 = createFrame11()
    frame12 = createFrame12()

    global_var.root_window.mainloop()