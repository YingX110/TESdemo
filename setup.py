'''
Read user input daat from spreadsheet
constract proc_info as below
'''
import pandas as pd
import numpy as np


xl = pd.ExcelFile('./user_input_data/input_template.xlsx')


def df_dic(df):
    # df = df.dropna()
    # df = df.T.reset_index()
    df.columns = ['cat', 'val']
    return dict(zip(df.cat,df.val))


# def add_nested_dict(main, new):
#     for name, ele in new.items():
#         for k in main.keys():
#             main[k][name] = ele[k]
#     return main


def dic_process(xl):
    sheets = xl.sheet_names
    LCAsys = {} 

    for st in sheets:
        df = xl.parse(st) 
        ESs = list(df.ES.unique())
        scale_es = {}
        sp_es = {}
        for es in ESs:
            dfe = df[df['ES'] == es]
            gen_col = ['ES','name','location','sharing principle method','ES local supply','final demand']
            scale_col = ['scales-general','scales-specific']
            sp_col = ['SP info-name','SP info-amount']
            dfmain = dfe.loc[:, gen_col]
            dfscale = dfe.loc[:, scale_col]
            dfsp = dfe.loc[:, sp_col]

            dfmain = dfmain.dropna().T.reset_index()
            dfmain = dfmain.drop([0])
            dfscale = dfscale.dropna()
            dfsp = dfsp.dropna()

            dicmain = df_dic(dfmain)
            scale_es.update({es: df_dic(dfscale)})
            sp_es.update({es: df_dic(dfsp)})

        dicscale = {'scales': scale_es}
        dicsp = {'SP info': sp_es}

        process = dicmain | dicscale | dicsp
    
    LCAsys.udate(process)
    
    return LCAsys


process_info = dic_process(xl)
print('done!')


# def get_intv(list, r):
#     list = [0] + list + [r]
#     res = []
#     for i in range(len(list)-1):
#         intv = range(list[i], list[i+1])
#         res.append(intv)
#     return res



# def dic_process(xl):
#     sheets = xl.sheet_names
    
#     for st in sheets:
#         data = xl.parse(st) 
#         pos = data.index[~data['L1'].isnull()].tolist()
#         lst_intv = get_intv(pos, data.shape[0])
#         gen = data.iloc[lst_intv[0], :]
#         scl = data.iloc[lst_intv[1], :]
#         sp = data.iloc[lst_intv[2], :]

#         ESs = list(data.columns)[2: ] # list of ES names
#         scl = scl.dropna(subset=ESs, how='all').dropna(axis=1, how='all')
       


#######################################################################################


# data =  pd.read_csv('./user_input_data/process_info.csv', index_col=0)

# proc = {
#     'name': 'State',
#     'location': 'Ohio',
#     'type': 'Geo-unit process',
#     'sharing principle method': 'population',
#     'ES local supply': None,
#     'final demand': None,
#     'scales': {
#         'carbon sequestration': {
#             'World': 'World'
#         }
#     }
# }

# procs = {
#     '001':{
#         'name': 'fertilizer',
#         'location': 'xx st, Wisconsin', # address for checking whether user input info is correct, not directly used for LCA system
#         'type': 'LCA',
#         'sharing principle method': 'population',
#         'ES local supply': {
#             'carbon sequestration': 3200
#         },
#         'final demand': 0,
#         'scales': {
#             'carbon sequestration': {
#                 'State': 'Wisconsin',
#                 'World': 'World'
#             }
#         },
#         'SP info': {
#             'carbon sequestration': {
#                 'demand': 6400,
#                 'population': 100,
#                 'gdp': 50000,
#                 'inverse gdp': 1/50000,
#                 'area': 2000
#             }
#         }
#     },
#     '002':{
#         'name': 'corn',
#         'location': 'xx rd, Ohio',
#         'type': 'LCA',
#         'sharing principle method': 'population',
#         'ES local supply': {
#             'carbon sequestration': 5500
#         },
#         'final demand': 0,
#         'scales': {
#             'carbon sequestration': {
#                 'State': 'Ohio',
#                 'World': 'World'
#             }
#         },
#         'SP info': {
#             'carbon sequestration': {
#                 'demand': 11000,
#                 'population': 86,
#                 'gdp': 60000,
#                 'inverse gdp': 1/60000,
#                 'area': 2700
#             }
#         }
#     },
#     '003':{
#         'name': 'ethanol',
#         'location': 'xx rd, Ohio',
#         'type':'LCA',
#         'sharing principle method': 'population',
#         'ES local supply': {
#             'carbon sequestration': 2100
#         },
#         'final demand': 2000,
#         'scales': {
#             'carbon sequestration': {
#                 'State': 'Ohio',
#                 'World': 'World'
#             }
#         },
#         'SP info': {
#             'carbon sequestration': {
#                 'demand': 4200,
#                 'population': 101,
#                 'gdp': 80000,
#                 'inverse gdp': 1/80000,
#                 'area': 3900
#             }
#         }
#     }
# }