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


@dataclass
class Vaccine :

    @staticmethod
    def createRandomListOfVaccination():
        with open("txts\\namesRight.txt","r") as nomi, open("txts\\surnamesRight.txt","r") as cognomi:
            try:
                list_of_vaccinations = []
                    
                brand_vacc = conf.vaccines[randint(0, len(conf.vaccines) - 1)]

                """for i in range(0, conf.max_number_of_vaccines):
                    list_of_vaccinations.append(Vaccine(brand_vacc, randint(500, 1000000), returnRandomDate(), ))"""
                    
            except:
                print("ERROR WHILE OPENING FILE IN CREATE RANDOM LIST OF VACCINATIONS")
                return
        




    brand : str
    lot : int
    date : datetime.date
    location : str
    cf_doctor : str



@dataclass
class Test :

    test_type : str
    date : datetime.date
    location : str
    result : bool
    cf_doctor : str



def returnRandomDate():

    random_number_of_days = rm.randrange(conf.days_between_dates)
    random_date = conf.start_date + datetime.timedelta(days=random_number_of_days)

    return random_date


@dataclass
class Person :

    @staticmethod
    def createPerson(name, surname, place_of_birth):

        age = abs(int(np.random.normal(45, 30)))

        if(age > 12 and conf.vaccine_probability > random()):
            person = Person(name, surname, age, place_of_birth ,conf.vaccines[randint(0, len(conf.vaccines) - 1)], randint(1, 4))
            return person

        else:
            person = Person(name, surname, age, "no vaccine", 0)
            return person


    name : str
    surname : str
    age : int
    place_of_birth : str
    vaccines : List(Vaccine)
    tests : List(Test)


