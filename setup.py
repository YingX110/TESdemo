'''
Read user input daat from spreadsheet
constract proc_info as below
'''
import pandas as pd

data =  pd.read_csv('./user_input_data/process_info.csv', index_col=0)

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