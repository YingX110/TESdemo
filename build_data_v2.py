import pandas as pd

geo_unit = ['County', 'State', 'Country', 'World', 'Watershed'] # expand this list when more ESs are added to the ecological data inventory

'''
To do: remove unnecessary white space 
'''

# def format_process(ls_df):
#     flag = 0
#     for df in ls_df:
#         ESname = df.ES.unique()[0]
#         if flag == 0:
#             dictcom = df[['name', 'location', 'type', 'final demand']].to_dict('index')
#         dictes = df[['SP name', 'SP amount', 'local demand', 'local supply']].to_dict('index')
#         dictscale = df[geo_unit].dropna(axis='columns').to_dict('index')
        
#         for k, v in dictcom.items():
#             # v[ESname] = dfes.loc[[k]].to_dict('index')[k]
#             if flag == 0:
#                 v['ES'] = {}
#             v['ES'][ESname] = dictes[k]
#             v['ES'][ESname]['scales'] = dictscale[k]
        
#         flag += 1
#     return dictcom



def format_process(ls_df):
    flag = 0
    ls_ES = []
    for df in ls_df:
        ESname = df.ES.unique()[0]
        ls_ES.append(ESname)
        if flag == 0:
            dictcom = df[['name', 'location', 'type', 'final demand']].to_dict('index')
            location = df[['name', 'location']].reset_index().drop(['index'], axis=1)
            flag += 1
        dictes = df[['SP name', 'SP amount', 'local demand', 'local supply']].to_dict('index')
        dictscale = df[geo_unit].dropna(axis='columns').to_dict('index')
        
        for k, v in dictcom.items():
            v[ESname] = dictes[k]
            v[ESname]['scales'] = dictscale[k]
            v['ES'] = ls_ES 
    dictcom['Address'] = location    
    return dictcom
    

if __name__ == '__main__':
    df1 = pd.read_csv('ES1_info.csv', index_col=0)
    df2 = pd.read_csv('ES2_info.csv', index_col=0)
    ls_df = [df1, df2]
    res = format_process(ls_df)


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