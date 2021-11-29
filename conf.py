import datetime



#initial date and final date
start_date = datetime.date(2020, 3, 1)
end_date = datetime.date(2020, 3, 30)
time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days


start_birthdate = datetime.date(1900, 1, 1)
end_birthdate = datetime.date(2021, 12, 31)
time_between_birthdates = end_birthdate - start_birthdate
days_between_birthdates = time_between_birthdates.days





vaccines = ('Pfizer', 'Astrazeneca', 'Moderna', 'Sputnik')
vaccine_probability = 0.7
max_number_of_days_between_production_and_use_of_vaccine = 80
max_number_of_vaccines = 4
type_of_test = ("MOLECULAR_TEST", "ANTIGEN_TEST", "ANTIBODY_TEST")
max_number_of_tests = 5
probability_positive_test_result = 0.1




type_of_authbody = ('Pharmacy', 'Hospital', 'Clinic')
max_number_of_doctor_per_auth_body = 5



