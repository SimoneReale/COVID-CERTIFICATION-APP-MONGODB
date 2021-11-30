from xmlrpc.client import Boolean
import pymongo
from random import randint, random
from tkinter.ttk import Progressbar
import conf
import numpy as np
import datetime
import random as rm
import traceback
import descrizione as descr


def createAuthorizedBody(active, location, type, list_of_doctors):
    dict_auth = {'active' : active, 'location' : location, 'type' : type, 'list_of_doctors' : list_of_doctors}
    return dict_auth

def createVaccine(brand, lot, date, production_date,  location, cf_doctor):
    dict_vaccine = {'brand' : brand, 'lot' : lot, 'date' : date, 'production_date' : production_date,  'location' : location, 'cf_doctor' : cf_doctor}
    return dict_vaccine

def createTest(test_type, date, location, result, cf_doctor):
    dict_test = {'test_type' : test_type, 'date' : date, 'location' : location, 'result' : result, 'cf_doctor' : cf_doctor}
    return dict_test

def createPerson(name, surname, birthdate, details, list_of_vaccinations, list_of_tests):
    dict_person = {'name' : name, 'surname' : surname, 'birthdate' : birthdate, 'details' : details, 'list_of_vaccinations' : list_of_vaccinations, 'list_of_tests' : list_of_tests}
    return dict_person




def returnRandomDate():

    random_number_of_days = rm.randrange(conf.days_between_dates)
    random_date = conf.start_date + datetime.timedelta(days=random_number_of_days)

    return random_date


def returnRandomBirthDate():

    random_number_of_days = rm.randrange(conf.days_between_birthdates)
    random_birthdate = conf.start_birthdate + datetime.timedelta(days=random_number_of_days)

    return random_birthdate



def returnCertificateExpirationDate(dict_person):

    
    if len(dict_person['list_of_tests']) == 0 and len(dict_person['list_of_vaccinations']) == 0:
        return None

    elif len(dict_person['list_of_tests']) == 0 and len(dict_person['list_of_vaccinations']) > 0:
        sorted_list_of_vaccinations = sorted(dict_person['list_of_vaccinations'], key=lambda d: datetime.datetime.strptime(d['date'], "%Y-%m-%d").date()) 
        last_vaccine = sorted_list_of_vaccinations[-1]
        last_vaccine_date = datetime.datetime.strptime(last_vaccine['date'], "%Y-%m-%d").date()
        return last_vaccine_date + datetime.timedelta(days=conf.validity_of_vaccine_number_of_days)


    elif len(dict_person['list_of_tests']) > 0 and len(dict_person['list_of_vaccinations']) == 0:
         sorted_list_of_tests = sorted(dict_person['list_of_tests'], key=lambda d: datetime.datetime.strptime(d['date'], "%Y-%m-%d").date()) 
         last_test = sorted_list_of_tests[-1]

         if last_test['result'] == True:
            return None

         else:
            last_test_date = datetime.datetime.strptime(last_test['date'], "%Y-%m-%d").date()
            return last_test_date + datetime.timedelta(days=conf.validity_of_test_number_of_days)



    else:
        sorted_list_of_vaccinations = sorted(dict_person['list_of_vaccinations'], key=lambda d: datetime.datetime.strptime(d['date'], "%Y-%m-%d").date()) 
        sorted_list_of_tests = sorted(dict_person['list_of_tests'], key=lambda d: datetime.datetime.strptime(d['date'], "%Y-%m-%d").date()) 

        last_test = sorted_list_of_tests[-1]
        last_vaccine = sorted_list_of_vaccinations[-1]

        if last_test['result'] == True:
            return None

        last_test_date = datetime.datetime.strptime(last_test['date'], "%Y-%m-%d").date()
        last_vaccine_date = datetime.datetime.strptime(last_vaccine['date'], "%Y-%m-%d").date()

        validity_date = last_test_date + datetime.timedelta(days=conf.validity_of_test_number_of_days) if last_test_date > last_vaccine_date + datetime.timedelta(days=conf.validity_of_vaccine_number_of_days) else last_vaccine_date + datetime.timedelta(days=conf.validity_of_vaccine_number_of_days)

        return validity_date











def createDataset(number_of_people, db):
    with open("txts\\namesRight.txt","r") as nomi, open("txts\\surnamesRight.txt","r") as cognomi, open("txts\\places.txt","r") as vie, open("txts\\capoluoghi.txt","r") as capoluoghi:
            
            try:

                lista_nomi = nomi.readlines()
                lista_cognomi = cognomi.readlines()
                lista_vie = vie.readlines()
                
                #creo gli auth_bod
                list_of_authbod = []
                #minimo 2 auth bod in ogni caso 
                for j in range(0, int(number_of_people / 6) + 2):
                    list_of_doctors_auth_bod = []
                    #almeno un medico in ogni auth bod
                    for f in range(0, randint(0, conf.max_number_of_doctor_per_auth_body) + 1):
                        doctor = rm.choice(lista_nomi).strip('\n') + " " +rm.choice(lista_cognomi).strip('\n')
                        list_of_doctors_auth_bod.append(doctor)

                    list_of_authbod.append(createAuthorizedBody(True, rm.choice(lista_vie).strip('\n'), 
                                           conf.type_of_authbody[randint(0, len(conf.type_of_authbody) - 1)], list_of_doctors_auth_bod))

                #inserisco nel database gli authorized bodies
                col_authBod = db['AuthorizedBodies_Collection']
                col_authBod.insert_many(list_of_authbod)



                list_of_people = []

                for i in range(0, number_of_people):

                    person_name = lista_nomi[i].strip('\n')
                    
                    person_surname = rm.choice(lista_cognomi).strip('\n')
                    birthdate = str(returnRandomBirthDate())

                
                    list_of_vaccinations = []
                        
                    brand_vacc = rm.choice(conf.vaccines)

                    for i in range(0, randint(0, conf.max_number_of_vaccines)):
                        vacc_lot = randint(500, 10000000)
                        auth_bod = rm.choice(list_of_authbod)
                        list_of_doc = auth_bod['list_of_doctors']

                        date = returnRandomDate()

                        production_date = date - datetime.timedelta(days= randint(0, conf.max_number_of_days_between_production_and_use_of_vaccine))

                        vaccine = createVaccine(brand_vacc, vacc_lot, str(returnRandomDate()), str(production_date), auth_bod['location'], list_of_doc[randint(0, len(list_of_doc) - 1)])
                        list_of_vaccinations.append(vaccine)


                    list_of_tests = []

                    for k in range(0, randint(0, conf.max_number_of_tests)):
                        auth_bod = rm.choice(list_of_authbod)
                        list_of_doc = auth_bod['list_of_doctors']
                        test_result = True if random() < conf.probability_positive_test_result else False
                        test = createTest(rm.choice(conf.type_of_test), str(returnRandomDate()), auth_bod['location'], test_result, rm.choice(list_of_doc))
                        list_of_tests.append(test)

                    person_details = descr.returnFraseDescrizione()
                    person = createPerson(person_name, person_surname, birthdate, person_details, list_of_vaccinations, list_of_tests)
                    list_of_people.append(person)


                #inserisco nel database le persone
                col_authBod = db['Certificate_Collection']
                col_authBod.insert_many(list_of_people)
                
                
                return list_of_people

            except Exception:
                print(traceback.format_exc())
                print("ERROR WHILE OPENING FILE IN CREATE RANDOM LIST OF VACCINATIONS")
                return