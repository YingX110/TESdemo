# import pandas as pd
import requests
import urllib 

api_key = 'AIzaSyBvLbmMG9h3gLt66cdP-T1Sda9TUMGmgyY'

# df = pd.read_csv('locations.csv')
def get_location(df):
    df = df.dropna()

    for i, row in df.iterrows():
        address = df.loc[i, 'location']
        encoded_address = urllib.parse.quote(address)
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+encoded_address+'&key='+api_key)
        resp_json = response.json()
        lat = (resp_json['results'][0]['geometry']['location']['lat'])
        lng = (resp_json['results'][0]['geometry']['location']['lng'])

        df.loc[i,'lat'] = lat
        df.loc[i,'lng'] = lng
    
    return df



 