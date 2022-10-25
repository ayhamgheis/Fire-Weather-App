import sys 
from tracemalloc import start
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import sys
from datetime import date
from datetime import timedelta



#----------------------------------------------------- Web Scraper --------------------------------------------------------------#

#User input defines start and end date for crd data request
#format is YYYYmmDDhhmm (eg. 201809010015)
'''
YYYY- year (eg. 2018)
mm - month (eg. 09)
DD - day (eg. 01)
hh - hour (eg. 00)
mm - minute (eg. 15)
'''
def get_dates():

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
    
    scrape(url, start_date, end_date, dates_provided)



def scrape(url, start_date, end_date, dates_provided):

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

#----------------------------------------------------- Web Scraper --------------------------------------------------------------#




#----------------------------------------------------- CSV merge --------------------------------------------------------------#
def combine():
   
    #input filename for fts 360 data and create corresponding dataframe
    fts = input ("Enter FTS 360 filename: ")
    fts_dataframe = pd.read_csv(fts)

    #input filename for crd data and create corresponding dataframe
    crd = input("Enter CRD filename: ")
    crd_dataframe = pd.read_csv(crd)

    # merge the two dataframes
    merge = pd.concat([crd_dataframe, fts_dataframe])

    #generate and print output file name
    crd_name = crd.split(".")
    fts_name = fts.split(".")
    merged_filename = f'{fts_name[0]}_{crd_name[0]}_merged.csv'
    print(merged_filename)

    #convert merged dataframes to csv file and write to output filename
    merge.to_csv(merged_filename, index= False)



    #df = pd.concat(
    #map(pd.read_csv, [fts_dataframe, crd_dataframe]), ignore_index=True)


    #df.to_csv('merged.csv', index = False)

    
    
#----------------------------------------------------- CSV merge --------------------------------------------------------------#


def run():
    if (sys.argv[1] == 'scrape'):
        get_dates()

    elif (sys.argv[1] == 'merge'):
        combine()
    else:
        sys.exit('command line argument invalid, please provide one of the following: merge or scrape')

    

if __name__== '__main__':
    run()
