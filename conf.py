import datetime



string_mongodb = "mongodb+srv://<user>:<password>@clustercovid.bbrjj.mongodb.net/CovidDatabase?retryWrites=true&w=majority"


#initial date and final date
start_date = datetime.date(2020, 3, 1)
end_date = datetime.date(2020, 3, 15)
time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days





vaccines = ('Pfizer', 'Astrazeneca', 'Moderna', 'Sputnik')
vaccine_probability = 0.7
max_number_of_vaccines = 4



