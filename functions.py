from xmlrpc.client import Boolean
import pymongo
from dataclasses import dataclass
from random import randint, random
from tkinter.ttk import Progressbar
from py2neo import Graph, NodeMatcher
import conf
import numpy as np
import datetime
import random as rm
from typing import List
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



@dataclass
class Certificate :

    @staticmethod
    def createCertificate(name, surname, place_of_birth, vaccines, tests):

        age = abs(int(np.random.normal(45, 30)))

        if(age > 12 and conf.vaccine_probability > random()):
            person = Certificate(name, surname, age, place_of_birth ,conf.vaccines[randint(0, len(conf.vaccines) - 1)], randint(1, 4))
            return person

        else:
            person = Certificate(name, surname, age, place_of_birth, "no vaccine", tests)
            return person


    name : str
    surname : str
    age : int
    place_of_birth : str
    vaccines : str
    tests : str






def createDataset(number_of_people, db):
    with open("txts\\namesRight.txt","r") as nomi, open("txts\\surnamesRight.txt","r") as cognomi, open("txts\\places.txt","r") as vie, open("txts\\capoluoghi.txt","r") as capoluoghi:
            
            try:

                lista_nomi = nomi.readlines()
                len_nomi = len(lista_nomi) - 1
                lista_cognomi = cognomi.readlines()
                len_cognomi = len(lista_cognomi) - 1
                lista_vie = vie.readlines()
                len_vie = len(lista_vie) - 1
                
                #creo gli auth_bod
                list_of_authbod = []
                for j in range(0, int(number_of_people / 6) + 2):
                    list_of_doctors_auth_bod = []
                    for f in range(0, randint(0, conf.max_number_of_doctor_per_auth_body) + 1):
                        doctor = lista_nomi[randint(0, len_nomi)].strip('\n') + " " +lista_cognomi[randint(0, len_cognomi)].strip('\n')
                        list_of_doctors_auth_bod.append(doctor)

                    list_of_authbod.append(createAuthorizedBody(True, lista_vie[randint(0, len_vie)].strip('\n'), 
                                           conf.type_of_authbody[randint(0, len(conf.type_of_authbody) - 1)], list_of_doctors_auth_bod))

                #inserisco nel database gli authorized bodies
                col_authBod = db['AuthorizedBodies_Collection']
                col_authBod.insert_many(list_of_authbod)



                list_of_people = []

                for i in range(0, number_of_people):

                    person_name = lista_nomi[randint(0, len_nomi)].strip('\n')
                    person_surname = lista_cognomi[randint(0, len_cognomi)].strip('\n')
                    birthdate = str(returnRandomBirthDate())

                
                    list_of_vaccinations = []
                        
                    brand_vacc = conf.vaccines[randint(0, len(conf.vaccines) - 1)]

                    for i in range(0, randint(0, conf.max_number_of_vaccines)):
                        vacc_lot = randint(500, 10000000)
                        auth_bod = list_of_authbod[randint(0, len(list_of_authbod) - 1)]
                        list_of_doc = auth_bod['list_of_doctors']

                        date = returnRandomDate()

                        production_date = date - datetime.timedelta(days= randint(0, conf.max_number_of_days_between_production_and_use_of_vaccine))

                        vaccine = createVaccine(brand_vacc, vacc_lot, str(returnRandomDate()), str(production_date), auth_bod['location'], list_of_doc[randint(0, len(list_of_doc) - 1)])
                        list_of_vaccinations.append(vaccine)


                    list_of_tests = []

                    for k in range(0, randint(0, conf.max_number_of_tests)):
                        auth_bod = list_of_authbod[randint(0, len(list_of_authbod) - 1)]
                        list_of_doc = auth_bod['list_of_doctors']
                        test_result = True if random() < conf.probability_positive_test_result else False
                        test = createTest(conf.type_of_test[randint(0, len(conf.type_of_test) - 1)], str(returnRandomDate()), auth_bod['location'], test_result, list_of_doc[randint(0, len(list_of_doc) - 1)])
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