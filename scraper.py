from tracemalloc import start
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import sys
from datetime import date
from datetime import timedelta


#User input defines start and end date for crd data request
#format is YYYYmmDDhhmm (eg. 201809010015)
'''
YYYY- year (eg. 2018)
mm - month (eg. 09)
DD - day (eg. 01)
hh - hour (eg. 00)
mm - minute (eg. 15)
'''
start_date = input("Enter a start date: ")
end_date = input("Enter an end date: ")
dates_provided = True
url = f'https://webservices.crd.bc.ca/weatherdata/UVIC_20220413/{start_date}-{end_date}'


#if no dates are provided the default data access is for the past 28 days from the current day
if(start_date == '' and end_date ==''):
    url = 'https://webservices.crd.bc.ca/weatherdata/UVIC_20220413'
    dates_provided = False
#check date formatting
elif(len(start_date) != 12):
    sys.exit('Start date is not valid')
elif(len(end_date) != 12):
    sys.exit('End date is not valid')

#send a get request to crd url and scrape data from said url
r =requests.get(url)
soup = str(BeautifulSoup(r.content, 'html.parser'))

# load scraped data into json object
data = json.loads(soup)
json_object = json.dumps(data['DATA'], indent =4)

if(dates_provided):
    #write json object to json file
    json_filename = f'{start_date}-{end_date}.json'
    with open(json_filename,"w") as outfile:
        outfile.write(json_object)
    print(json_filename)

    #convert json file to csv file
    csv_filename = f'{start_date}-{end_date}.csv'
    pandas_object = pd.read_json(json_filename, orient ='records')
    pandas_object.to_csv(csv_filename,index=False)
    print(csv_filename)


else:
    today = date.today()
    start = today - timedelta( days= 28)

    start_date = start.strftime("%Y%m%d" +"0000")
    end_date = today.strftime("%Y%m%d"+"0000")
    json_filename = f'{start_date}-{end_date}.json'

    with open(json_filename,"w") as outfile:
        outfile.write(json_object)
    print(json_filename)

    #convert json file to csv file
    csv_filename = f'{start_date}-{end_date}.csv'
    pandas_object = pd.read_json(json_filename, orient ='records')
    pandas_object.to_csv(csv_filename,index=False)
    print(csv_filename)
