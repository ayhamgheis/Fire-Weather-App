import pandas as pd

def combine():
   
    #input filename for fts 360 data and create corresponding dataframe
    fts = input ("Enter FTS 360 filename: ")
    fts_dataframe_raw = pd.read_csv(fts)
    fts_dataframe = fts_dataframe_raw.rename(columns=
    {"StationID": "RecordID", 
    "PARavg":"SolarActiveRadiation", 
    "PYRavg":"SolarRadiation", 
    "RnTotal":"Rain", 
    "Dir": "WindDirection",
     "Wspd" :"WindSpeed", 
     "Temp": "AirTemperature", 
     "Rh": "RelativeHumidity",}
     )
    


    #input filename for crd data and create corresponding dataframe
    crd = input("Enter CRD filename: ")
    crd_data = pd.read_csv(crd)
    coords = pd.read_csv('coords.csv')
    crd_dataframe = pd.merge(crd_data, coords, on='StationName', how='inner')

    # merge the two dataframes
    merge = pd.concat([crd_dataframe, fts_dataframe])

    #generate and print output file name
    crd_name = crd.split(".")
    fts_name = fts.split(".")
    merged_filename = f'{fts_name[0]}_{crd_name[0]}_merged.csv'
    print(merged_filename)

    #convert merged dataframes to csv file and write to output filename
    merge.to_csv(merged_filename, index= False)


if __name__== '__main__':
    combine()
