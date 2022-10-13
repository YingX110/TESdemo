import pandas as pd
import requests
import urllib 

api_key = 'xxxxxx'

# df = pd.read_csv('location.csv')
def get_location(df):
    for i, row in df.iterrows():
        address = str(df.at[i,'Address'])  
        encoded_address = urllib.parse.quote(address)
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+encoded_address+'&key='+api_key)
        resp_json = response.json()
        lat = (resp_json['results'][0]['geometry']['location']['lat'])
        lng = (resp_json['results'][0]['geometry']['location']['lng'])

        df.at[i,'lat'] = lat
        df.at[i,'lng'] = lng