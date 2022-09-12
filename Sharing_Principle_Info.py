import pandas as pd
import numpy as np
import json

'''
!!! Todo:
should change 'emission' --> 'local demand' in all spreadsheet
to match with the name in demo3.py
'''

county_pop = pd.read_csv('./data/County_Pop.csv', index_col=0)
county_area = pd.read_csv('./data/County_Area.csv', index_col=0)
county_gdp = pd.read_csv('./data/County_GDP.csv', index_col=0)
county_invgdp = pd.read_csv('./data/County_invGDP.csv', index_col=0)
county_Dmd_C = pd.read_csv('./data/County_Emi.csv', index_col=0)

county_PrivC = pd.read_csv('./data/County_PrivC.csv', index_col=0)
county_PubC = None

county_info = [county_pop, county_area, county_gdp, county_invgdp, county_Dmd_C, county_PrivC, county_PubC]


###############################################################################
state_pop = pd.read_csv('./data/State_Pop.csv', index_col=0)
state_area = pd.read_csv('./data/State_Area.csv', index_col=0)
state_gdp = pd.read_csv('./data/State_GDP.csv', index_col=0)
state_invgdp = pd.read_csv('./data/State_invGDP.csv', index_col=0)
state_Dmd_C  = pd.read_csv('./data/State_Emi.csv', index_col=0)

state_PubC = pd.read_csv('./data/State_PubC.csv', index_col=0)
state_PrivC = pd.read_csv('./data/State_PrivC.csv', index_col=0)

state_info = [state_pop, state_area, state_gdp, state_invgdp, state_Dmd_C, state_PrivC, state_PubC]


###############################################################################
country_pop = pd.read_csv('./data/Nation_Pop.csv', index_col=0)
country_area = pd.read_csv('./data/Nation_Area.csv', index_col=0)
country_gdp = pd.read_csv('./data/Nation_GDP.csv', index_col=0)
country_invgdp = pd.read_csv('./data/Nation_invGDP.csv', index_col=0)
country_Dmd_C  = pd.read_csv('./data/Nation_Emi.csv', index_col=0)

country_PubC = pd.read_csv('./data/Nation_PubC.csv', index_col=0)
country_PrivC = pd.read_csv('./data/Nation_PrivC.csv', index_col=0)

country_info = [country_pop, country_area, country_gdp, country_invgdp, country_Dmd_C, country_PrivC, country_PubC]


###############################################################################
world_pop = pd.read_csv('./data/World_Pop.csv', index_col=0)
world_area = pd.read_csv('./data/World_Area.csv', index_col=0)
world_gdp = pd.read_csv('./data/World_GDP.csv', index_col=0)
world_invgdp = pd.read_csv('./data/World_invGDP.csv', index_col=0)
world_Dmd_C  = pd.read_csv('./data/World_Emi.csv', index_col=0)

world_PubC = pd.read_csv('./data/World_PubC.csv', index_col=0)
world_PrivC = pd.read_csv('./data/World_PrivC.csv', index_col=0)

world_info = [world_pop, world_area, world_gdp, world_invgdp, world_Dmd_C, world_PrivC, world_PubC]


###############################################################################
'''this is fake number'''
watershed_pop = pd.read_csv('./data/State_Pop.csv', index_col=0)
watershed_area = pd.read_csv('./data/State_Area.csv', index_col=0)
watershed_gdp = pd.read_csv('./data/State_GDP.csv', index_col=0)
watershed_invgdp = pd.read_csv('./data/State_invGDP.csv', index_col=0)
watershed_Dmd_C  = pd.read_csv('./data/State_Emi.csv', index_col=0)

watershed_PubC = pd.read_csv('./data/State_PubC.csv', index_col=0)
watershed_PrivC = pd.read_csv('./data/State_PrivC.csv', index_col=0)

watershed_info = [watershed_pop, watershed_area, watershed_gdp, watershed_invgdp, watershed_Dmd_C, watershed_PrivC, watershed_PubC]




def SP_dict(ls):
    df = pd.concat(ls, sort=False)
    return df.to_dict()

county = SP_dict(county_info)
state = SP_dict(state_info)
country = SP_dict(country_info)
world = SP_dict(world_info)
watershed = SP_dict(watershed_info)

SP_info = {
    'County': county,
    'State': state,
    'Country': country,
    'World': world,
    'Watershed': watershed
}


json_object = json.dumps(SP_info, indent = 4) 
with open("SP_info2.json", "w") as outfile:
    json.dump(SP_info, outfile)



# SP_info = {
#     'County': {
#         '1001': {
#             'population': 15236715,
#             'area': 786957,
#             'gdp': None,
#             'inverse gdp': None,
#             'demand': 90000,
#             'public supply': 63212,
#             'private supply': 53212
#         },
#         '1003': {}
#     },
#     'State': {},
#     'Country': {},
#     'World': {},
#     'Watershed': {
#         '03262000 ': {
#             'population': 12000,
#             'area': 10000,
#             'gdp': 18291802,
#             'inverse gdp': 0.0002323,
#             'public supply': 2000000,
#             'private supply': 1000000
#         }
#     }
# }



