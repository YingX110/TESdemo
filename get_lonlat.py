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


if __name__ == '__main__':
    from main2 import *
    df_s1 = pd.read_csv('ES1_info.csv', index_col=0)
    ls_df1 = [df_s1]
 
    dfA = pd.read_csv('./user_input_data/tech_matrix1.csv', index_col=0) 
    dfD1 = pd.read_csv('./user_input_data/intv_matrix1.csv', index_col=0) 
    wt = pd.read_csv('./user_input_data/weighting_vec.csv', index_col=0)
    
    toy1 = format_process(ls_df1)
    obj1 = LcaSystem(toy1, dfA, dfD1, wt)
    obj1.add_process(SP_info)
    
    test = obj1.Address.copy()
    res = get_location(test)
    print('dead')

  
 