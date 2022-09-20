'''
Read user input daat from spreadsheet
constract proc_info as below
'''
import pandas as pd


xl_u = pd.ExcelFile('./user_input_data/input_uni.xlsx')
xl_s = pd.ExcelFile('./user_input_data/input_template0.xlsx')


def df_dic(df):
    df.columns = ['cat', 'val']
    return dict(zip(df.cat,df.val))


def dic_process(xl):
    sheets = xl.sheet_names
    LCAsys = {} 

    for st in sheets:
        df = xl.parse(st) 
        ESs = list(df.ES.unique())
        scale_es = {}
        sp_es = {}
        dicmeth = {}
        dicsloc = {}
        es_idx = 0

        for es in ESs:
            dfe = df[df['ES'] == es]
            scale_col = ['scales-general','scales-specific']
            sp_col = ['SP info-name','SP info-amount']
            spmeth = dfe.loc[dfe['ES'] == es, 'sharing principle method'].values[0]
            slocal = dfe.loc[dfe['ES'] == es, 'ES local supply'].values[0]
            dfscale = dfe.loc[:, scale_col]
            dfsp = dfe.loc[:, sp_col]

            if es_idx == 0:
                tech_col = ['name','location','final demand', 'type']
                dftech = dfe.loc[:, tech_col]
                dftech = dftech.dropna(how='all').T.reset_index() # note change
                dictech = df_dic(dftech)
                es_idx = 1

            dicmeth[es] = spmeth
            dicsloc[es] = slocal

            dfscale = dfscale.dropna()
            dfsp = dfsp.dropna()
            scale_es[es] = df_dic(dfscale)
            sp_es[es] = df_dic(dfsp)

        dicmeth = {'sharing principle method': dicmeth}
        dicsloc = {'ES local supply': dicsloc}
        dicscale = {'scales': scale_es}
        dicsp = {'SP info': sp_es}

        process = dictech | dicscale | dicsp | dicmeth | dicsloc
    
        LCAsys[st] = process
    
    return LCAsys



pro_u = dic_process(xl_u)
pro_s= dic_process(xl_s)

print('done!')

# def get_intv(list, r):
#     list = [0] + list + [r]
#     res = []
#     for i in range(len(list)-1):
#         intv = range(list[i], list[i+1])
#         res.append(intv)
#     return res



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
#     'process1':{
#         'name': 'fertilizer production',
#         'location': '100 SW st, Wisconsin', # address for checking whether user input info is correct, not directly used for LCA system
#         'final demand': 0,
#         'type': 'LCA',
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
#         },
#         'sharing principle method': {
#             'carbon sequestration': 'population'
#         },
#         'ES local supply': {
#             'carbon sequestration': 3200
#         }
#     },
#     'process2':{
#         'name': 'corn farm',
#         'location': '2800 NE Rd, Ohio',
#         'final demand': 0,
#         'type': 'LCA',
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
#         },
#         'sharing principle method': {
#             'carbon sequestration': 'populaltion'
#         },
#         'ES local supply': {
#             'carbon sequestration': 5500
#         }
#     },
#     'process3':{
#         'name': 'ethanol production',
#         'location': '150 wood st, Ohio',
#         'final demand': 2000,
#         'type':'LCA',
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
#         },
#         'sharing principle method': {
#             'carbon sequestration': 'population'
#         },
#         'ES local supply': {
#             'carbon sequestration': 2100
#         }
#     }
# }


