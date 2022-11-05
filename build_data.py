import pandas as pd
'''
To do: remove unnecessary white space 
HUC code should be str instead of number, need a step to convert 
'''

geo_unit = ['County', 'State', 'Country', 'World', 'Watershed'] # expand this list when more ESs are added to the ecological data inventory

def format_process(ls_df):
    flag = 0
    ls_ES = []
    SC = {}
    SPM = {}
    LOCS = {}

    for df in ls_df:
        ESname = df.ES.unique()[0]
        ls_ES.append(ESname)
        if flag == 0:
            name = df['name'].to_list()
            dictcom = df[['name', 'location', 'type', 'final demand']].to_dict('index')
            location = df[['name', 'location']].reset_index().drop(['index'], axis=1)
            type = df.type.unique()[0]
            flag += 1
        dictes = df[['SP name', 'SP amount', 'local demand', 'local supply']].to_dict('index') # keep local demand for unit process
        dictscale = df[geo_unit].dropna(axis='columns', how='all').to_dict('index')
        localS = df['local supply'].to_list()
        
        for k, v in dictcom.items():
            v[ESname] = dictes[k]
            v[ESname]['scales'] = dictscale[k]
            v['ES'] = ls_ES 
    
        SCALES = list(df[geo_unit].dropna(axis='columns', how='all').columns)
        strSCALES = ", ".join(str(x) for x in SCALES)
        SC[ESname] = strSCALES
        LOCS[ESname] = localS
        SPM[ESname] = df['SP name'].unique()[0]

    dictcom['Address'] = location   
    dictcom['SCALES'] = SC 
    dictcom['SPM'] = SPM
    dictcom['TYPE'] = type
    dictcom['PROC NAME'] = name
    dictcom['LOCAL S'] = LOCS
    
    return dictcom
    

if __name__ == '__main__':
   
    df1 = pd.read_csv('./user_input_data/process_BD.csv', index_col=0)
    # df2 = pd.read_csv('ES2_info.csv', index_col=0)
    ls_df = [df1]
    res = format_process(ls_df)
    print('dead already')


# sys = {
#     'process1':{
#         'name': 'K Fert production',
#         'local': 'Eddy county, NM',
#         'final demand': 0,
#         'ES': {
#             'carbon sequestration': {
#                 'SP name': 'demand',
#                 'SP amount': 0.000188,
#                 'local demand': 0.000188,
#                 'local supply': 1.36e-07,
#                 'scales': {'World': 'World'}
#             },
#             'water provision': {
#                 'SP name': 'demand',
#                 'SP amount': 129.37,
#                 'local demand': 8.721,
#                 'local supply': 5.426,
#                 'scales': {'Watershed': 15050303}
#             }
#         }
#     },
#     'process2': {...},
#     'process3': {...},
#     ...
# }