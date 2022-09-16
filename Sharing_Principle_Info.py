import pandas as pd
import numpy as np
import json

'''
!!! Todo:
should change 'emission' --> 'local demand' in all spreadsheet
to match with the name in demo3.py
'''

county_pop = pd.read_csv('./data_inventory/County_Pop.csv', index_col=0)
county_area = pd.read_csv('./data_inventory/County_Area.csv', index_col=0)
county_gdp = pd.read_csv('./data_inventory/County_GDP.csv', index_col=0)
county_invgdp = pd.read_csv('./data_inventory/County_invGDP.csv', index_col=0)
county_Dmd_C = pd.read_csv('./data_inventory/County_Emi_C.csv', index_col=0)

county_TotalC = pd.read_csv('./data_inventory/County_TotalC.csv', index_col=0)
county_PubC = pd.read_csv('./data_inventory/County_PubC.csv', index_col=0)

county_info = [county_pop, county_area, county_gdp, county_invgdp]
county_dmd = [county_Dmd_C]
# county_supply = [county_PubC, county_TotalC]
county_pubS = [county_PubC]
county_totS = [county_TotalC]


###############################################################################
state_pop = pd.read_csv('./data_inventory/State_Pop.csv', index_col=0)
state_area = pd.read_csv('./data_inventory/State_Area.csv', index_col=0)
state_gdp = pd.read_csv('./data_inventory/State_GDP.csv', index_col=0)
state_invgdp = pd.read_csv('./data_inventory/State_invGDP.csv', index_col=0)
state_Dmd_C  = pd.read_csv('./data_inventory/State_Emi_C.csv', index_col=0)

state_PubC = pd.read_csv('./data_inventory/State_PubC.csv', index_col=0)
state_TotalC = pd.read_csv('./data_inventory/State_TotalC.csv', index_col=0)


state_info = [state_pop, state_area, state_gdp, state_invgdp]
state_dmd = [state_Dmd_C]
state_pubS = [state_PubC]
state_totS = [state_TotalC]


###############################################################################
country_pop = pd.read_csv('./data_inventory/Nation_Pop.csv', index_col=0)
country_area = pd.read_csv('./data_inventory/Nation_Area.csv', index_col=0)
country_gdp = pd.read_csv('./data_inventory/Nation_GDP.csv', index_col=0)
country_invgdp = pd.read_csv('./data_inventory/Nation_invGDP.csv', index_col=0)
country_Dmd_C  = pd.read_csv('./data_inventory/Nation_Emi_C.csv', index_col=0)

country_PubC = pd.read_csv('./data_inventory/Nation_PubC.csv', index_col=0)
country_TotalC = pd.read_csv('./data_inventory/Nation_TotalC.csv', index_col=0)

country_info = [country_pop, country_area, country_gdp, country_invgdp]
country_dmd = [country_Dmd_C]
country_pubS = [country_PubC]
country_totS = [country_TotalC]


###############################################################################
world_pop = pd.read_csv('./data_inventory/World_Pop.csv', index_col=0)
world_area = pd.read_csv('./data_inventory/World_Area.csv', index_col=0)
world_gdp = pd.read_csv('./data_inventory/World_GDP.csv', index_col=0)
world_invgdp = pd.read_csv('./data_inventory/World_invGDP.csv', index_col=0)
world_Dmd_C  = pd.read_csv('./data_inventory/World_Emi_C.csv', index_col=0)

world_PubC = pd.read_csv('./data_inventory/World_PubC.csv', index_col=0)
world_TotalC = pd.read_csv('./data_inventory/World_TotalC.csv', index_col=0)

world_info = [world_pop, world_area, world_gdp, world_invgdp]
world_dmd = [world_Dmd_C]
world_pubS  = [world_PubC]
world_totS = [world_TotalC]


###############################################################################
'''this is fake number'''
watershed_pop = pd.read_csv('./data_inventory/Watershed_Pop.csv', index_col=0)
watershed_area = pd.read_csv('./data_inventory/Watershed_Area.csv', index_col=0)
watershed_gdp = pd.read_csv('./data_inventory/Watershed_GDP.csv', index_col=0)
watershed_invgdp = pd.read_csv('./data_inventory/Watershed_invGDP.csv', index_col=0)
watershed_Dmd_C  = pd.read_csv('./data_inventory/Watershed_Emi_C.csv', index_col=0)

watershed_PubC = pd.read_csv('./data_inventory/Watershed_PubC.csv', index_col=0)
watershed_TotalC = pd.read_csv('./data_inventory/Watershed_TotalC.csv', index_col=0)

watershed_info = [watershed_pop, watershed_area, watershed_gdp, watershed_invgdp]
watershed_dmd = [watershed_Dmd_C]
watershed_pubS = [watershed_PubC]
watershed_totS = [watershed_TotalC]


###############################################################################


# def SP_dict(ls_info, ls_dmd, ls_pub_sup, ls_total_sup, geoname):
#     dict_info = pd.concat(ls_info, sort=False).to_dict()
#     dict_dmd = pd.concat(ls_dmd, sort=False).to_dict()
#     dict_pub_sup = pd.concat(ls_pub_sup, sort=False).to_dict()
#     dict_total_sup = pd.concat(ls_total_sup, sort=False).to_dict()

#     dict_info['demand'] = dict_dmd
#     dict_info['public supply'] = dict_pub_sup 
#     dict_info['total supply'] = dict_total_sup 

#     res = {
#         geoname: dict_info
#     }

#     return res

# def df2dic(ls1, ls2):
#     df = pd.concat(ls1+ls2, sort=False).to_dict()
#     r = 0
#     for item in ls1:
#         r += item.shape[0]
#     dict1 = df.iloc[:r, :].to_dict()
#     dict2 = df.iloc[r:, :].to_dict()
#     return dict1, dict2




def df2dict(*args):
    '''
    Take in lists of dataframes,
    convert each list to a dictonary,
    return these dictionaries as one list.
    Number of dictonaries equals to the number of input lists
    '''
    N = []
    ls = []
    res = []
    for a in args:
        n = 0
        for df in a:
            n += df.shape[0]
            ls.append(df)
        N.append(n)
        
    data = pd.concat(ls, sort=False)
    head = 0
    for l in N:
        dict = data.iloc[head:head+l, :].to_dict()
        res.append(dict)
        head += l
    return res
        


# def add_nested_dict(main, new, keyname):
    
#     for k in main.keys():
#         main[k][keyname] = new[k]
    
#     return main

def add_nested_dict(main, new):
    for name, ele in new.items():
        for k in main.keys():
            main[k][name] = ele[k]
    return main



def SP_construct(info, dmd, pubS, totS):
    output = df2dict(info, dmd, pubS, totS)
    main, nest1, nest2, nest3 = output[0], output[1], output[2], output[3]
    NEST = {
        'demand': nest1,
        'public supply': nest2,
        'total supply': nest3
    }
    result = add_nested_dict(main, NEST)
    return result


county = SP_construct(county_info, county_dmd, county_pubS, county_totS)
state = SP_construct(state_info, state_dmd, state_pubS, state_totS)
country = SP_construct(country_info, country_dmd, country_pubS, country_totS)
world = SP_construct(world_info, world_dmd, world_pubS, world_totS)
watershed = SP_construct(watershed_info, watershed_dmd, watershed_pubS, watershed_totS)


# output = df2dict(county_info, county_demand, county_supply)
# main, nest1, nest2 = output[0], output[1], output[2]
# new = {
#     'demand': nest1,
#     'supply': nest2
# }

# RR = add_nested_dict(main, new)

    



# SP_info = {**county, **state, **country, **world, **watershed}
# SP_info = county | state | country | world | watershed
# print('done!')


SP_info = {
    'County': county,
    'State': state,
    'Country': country,
    'World': world,
    'Watershed': watershed
}


# json_object = json.dumps(SP_info, indent = 4) 
# with open("SP_info3.json", "w") as outfile:
#     json.dump(SP_info, outfile)



# SP_info = {
#     'County': {
#         '1001': {
#             'population': 15236715,
#             'area': 786957,
#             'gdp': None,
#             'inverse gdp': None,
#             'demand': {
#                 'carbon': 9000,
#                 'water': 200
#             },
#             'public supply': {
#                 'carbon': 63212,
#                 'water': 1462
#             },
#             'total supply': {
#                 'carbon': 452712,
#                 'water': 1234
#             }
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


