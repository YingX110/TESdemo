import pandas as pd
import numpy as np
from scipy.linalg import lu_factor, lu_solve
import json
from build_data_v2 import format_process
import plotly.express as px
from get_lonlat import *


f = open('SP_info4.json')
SP_info = json.load(f)



class Process:
    def __init__(self, info):
        self.name = info['name'] # this is used for geo-unit process: 'county', 'state', 'country'...
        self.type = info['type'] # LCA or geo unit
        self.location = info['location'] # this is used for geo-unit process: fips for county, state name for states
        self.f = info['final demand']
        self.ESname = info['ES']
        self.supply_disag = {}
        self.supply = {}
        self.all = info


    def cal_supply(self, SP_info):
        '''
        !! Todo:
        robust requirement: should consider none -> add a if condition

        ES: [C sequestration, Water provision...]
        sp_name: demand/population/area/gdp/inverse gdp
        '''
        
        for es in self.ESname:
            ESinfo = self.all[es] # for Ecosystem service X
            scales = ESinfo['scales']
            SP_meth = ESinfo['SP name']
            self.supply_disag[es] = {}

            if self.type == 'Geo-unit process':
                '''
                If a geo-unit (county/state/country...) be considered as 
                a unit process, local info are not required from users
                '''
                local_S = SP_info[self.name][self.location]['total supply'][es]
                if SP_meth == 'demand':
                    sp_amount_L = SP_info[self.name][self.location][SP_meth][es]
                else:
                    sp_amount_L = SP_info[self.name][self.location][SP_meth]
            else:
                local_S = ESinfo['local supply']
                sp_amount_L = ESinfo['SP amount']
            
            self.supply_disag[es]['local'] = local_S
            allo_S = 0
            frac = 1

            for k, v in scales.items(): 
                '''
                k: general scale name: County, State, Watershed...
                v: specific location name: Ohio, United States...
                S: supply at higher scales except local scale
                sp_amount_L: sharing principle (emission/population/area...) at smaller scale
                sp_amount_H: sharing principle (emission/population/area...) at larger scale
                '''
                S = SP_info[k][v]['public supply'][es]
                if SP_meth == 'demand': 
                    sp_amount_H = SP_info[k][v][SP_meth][es]
                else:
                    sp_amount_H = SP_info[k][v][SP_meth]
                frac = frac * (sp_amount_L / sp_amount_H)
                allo_S += frac * S
                sp_amount_L = sp_amount_H
                self.supply_disag[es][k] = frac * S
            self.supply[es] = allo_S + local_S
            # self.supply_disag[es]['total'] = allo_S + local_S



class LcaSystem:
    def __init__(self, PDic, dfA, dfD, wt):
        self.PDic = PDic
        self.Address = self.PDic.pop('Address') # need check!!!!!!!!!
        self.tech_matrix = dfA.values
        self.intv_matrix = dfD.values
        self.ProcNum = self.tech_matrix.shape[1] # number of processes - column
        self.FlowNum = self.intv_matrix.shape[0] 
        self.wt = wt.values[0] # import as a dataframe with one row, each col represents a process, col number equals to that of A matrix
        self.processes = []


    def add_process(self, SP_info):
        for p in self.PDic.values():
            process = Process(p)
            process.cal_supply(SP_info)
            self.processes.append(process)
            if len(self.processes) == 1: # number of ES should be the same for all processes, so only record once
                self.ESNum = len(p['ES'])


    @staticmethod
    def diag_mat(m1, m2):
        if m1.size == 0:
            return m2
        else:
            TR = np.zeros((m1.shape[0], m2.shape[1])) # zero matrix on top right
            LL = np.zeros((m2.shape[0], m1.shape[1])) # zero matrix on lower left
            up = np.hstack((m1, TR))
            down = np.hstack((LL, m2))
            return np.vstack((up, down))


    def WT_matrix(self):
        old = np.array([])
        for v in self.wt:
            new = np.ones((self.ESNum, 1)) * v 
            old = LcaSystem.diag_mat(old, new)
        self.wt_matrix = old


    def S_matrix(self):
        '''
        build S matrix from self.processes 
        for items in self.processes:
            ...
        !!! Todo:
        consider two cases: geo unit process and lca network
        '''
        self.WT_matrix()
        old = np.array([]) # empty array
        for p in self.processes:
            new = np.c_[list(p.supply.values())] # convert the list of supply to a vertical vector
            old = LcaSystem.diag_mat(old, new)
        self.supply_matrix = old * self.wt_matrix # dot product


    def f_matrix(self):
        '''
        final demand vector
        '''
        ls = []
        for proc in self.processes:
            ls.append(proc.f)
        Ft = np.c_[ls]
        self.Ft = Ft
   

    def tes_cal(self):
        '''
        construct large A D C S... matrix, use tes-lca framework
        do matrix calculation
        '''
        self.S_matrix()
        self.f_matrix()
        Ft = self.Ft
        S = self.supply_matrix
        A = self.tech_matrix
        D = self.intv_matrix
        me = np.ones((S.shape[1], 1))
        C = np.zeros((self.ProcNum, S.shape[1]))
        I = np.eye(self.FlowNum)
        O = np.zeros((self.ProcNum, self.FlowNum))

        AD = np.vstack((A,D))
        OI = np.vstack((O, -I))
        FO = np.vstack((Ft, np.zeros((self.FlowNum, 1))))
        CS = np.vstack((C, S))
        LHS = np.hstack((AD, OI))
        RHS = FO - CS @ me # matrix multiplication

        lu, piv = lu_factor(LHS)
        res = lu_solve((lu, piv), RHS)
        self.res = res

        return res
    


    def mapplot(self):
        loc = self.Address.copy()
        res = get_location(loc)
        
         



    def barplot(self, ES):
        lu, piv = lu_factor(self.tech_matrix)
        m = lu_solve((lu, piv), self.Ft)
        Dm = self.intv_matrix @ m
        demand = Dm.T[0].tolist()

        PName = []
        allo_s = 0
        local_s = 0
        for p in self.processes:
            sup = p.supply_disag
            temp = sup[ES]['total'] - sup[ES]['local']
            allo_s += temp
            local_s += sup[ES]['local']
            PName.append(p.name)
    

        supply = [0] * self.ProcNum
        supply.append(allo_s); supply.append(local_s)
        demand.append(0); demand.append(0)
        PName.append('allocated s'); PName.append('local s')

        data = {'Demand': demand, 'Supply': supply}
        df = pd.DataFrame.from_dict(data, orient='index', columns=PName)

        colors = px.colors.qualitative.T10
        fig = px.bar(df, 
            x = df.index,
            y = [c for c in df.columns],
            template = 'ggplot2',
            color_discrete_sequence = colors)
        return fig
        # fig.show()
        

       

if __name__ == '__main__':

    df_s1 = pd.read_csv('ES1_info.csv', index_col=0)
    df_s2 = pd.read_csv('ES2_info.csv', index_col=0)
    df_s2['Watershed'] = df_s2.Watershed.astype(str)
    ls_df1 = [df_s1]
    ls_df2 = [df_s1, df_s2]
    

    dfA = pd.read_csv('./user_input_data/tech_matrix1.csv', index_col=0) 
    dfD1 = pd.read_csv('./user_input_data/intv_matrix1.csv', index_col=0) # single ES
    dfD2 = pd.read_csv('./user_input_data/intv_matrix2.csv', index_col=0) # multiple ES
    wt = pd.read_csv('./user_input_data/weighting_vec.csv', index_col=0)
    
    toy1 = format_process(ls_df1)
    obj1 = LcaSystem(toy1, dfA, dfD1, wt)
    obj1.add_process(SP_info)
    
    toy2 = format_process(ls_df2)
    obj2 = LcaSystem(toy2, dfA, dfD2, wt)
    obj2.add_process(SP_info)

    res1 = obj1.tes_cal()
    res2 = obj2.tes_cal()
    # obj2.barplot('carbon sequestration')


    print('done!')








