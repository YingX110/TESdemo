'''
Read user input daat from spreadsheet
constract proc_info as below
'''
import pandas as pd

# xl_u = pd.ExcelFile('./user_input_data/input_uni.xlsx')
# xl_s = pd.ExcelFile('./user_input_data/input_template0.xlsx')


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
        es_No = 0

        for es in ESs:
            dfe = df[df['ES'] == es]
            scale_col = ['scales-general','scales-specific']
            sp_col = ['SP info-name','SP info-amount']
            spmeth = dfe.loc[dfe['ES'] == es, 'sharing principle method'].values[0]
            slocal = dfe.loc[dfe['ES'] == es, 'ES local supply'].values[0]
            dfscale = dfe.loc[:, scale_col]
            dfsp = dfe.loc[:, sp_col]

            if es_No == 0: # execute for the first ES on spreadsheet, these info are identical for all ESs
                tech_col = ['name','location','final demand', 'type']
                dftech = dfe.loc[:, tech_col]
                dftech = dftech.dropna(how='all').T.reset_index() # note change
                dictech = df_dic(dftech)
                es_No = 1

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

        if process['type'] == 'LCA': # seperate LCA system and Geo-unit process
            LCAsys[st] = process
        else:
            LCAsys = process
    return LCAsys



# pro_u = dic_process(xl_u)
# pro_s= dic_process(xl_s)

# print('done!')

# def get_intv(list, r):
#     list = [0] + list + [r]
#     res = []
#     for i in range(len(list)-1):
#         intv = range(list[i], list[i+1])
#         res.append(intv)
#     return res





