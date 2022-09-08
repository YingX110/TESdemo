import pandas as pd
import numpy as np
from numpy.linalg import inv



class Process:

    def build_proc(self, info):
        
        self.name = info['name'] # this is used for geo unit process: 'county', 'state', 'country'...
        self.type = info['type'] # LCA or geo unit
        self.location = info['location'] # this is used for geo unit process: fips for county, state name for states
        self.scales = info['scales']
        self.f = info['final demand']
        self.local_demand = info['SP info']['demand']
        self.local_supply = info['ES local supply']
        self.supply = {}


    def cal_supply(self, proc_info, SP_info):
        '''
        !! Todo:
        robust requirement: should consider none -> add a if condition

        ES_name: [C sequestration, Water provision...]
        sp_name: demand/population/area/gdp/inverse gdp
        '''
        type =  self.type
        scales = proc_info['scales'] 
        ES_name = list(scales.keys())
        sp_name = input('Name of sharing principle: ') 
        
        for es in ES_name:
            if type == 'Unit process':
                local_S = SP_info[self.name][self.location]['private supply']
                sp_amount_L = SP_info[self.name][self.location][sp_name]
            else:
                local_S = proc_info['ES local supply'][es]
                sp_amount_L  = proc_info['SP info'][sp_name]
            
            allo_S = 0
            frac = 1
            for k, v in scales[es].items(): 
                '''
                k: general scale name: County, State, Watershed...
                v: specific location name: Ohio, United States...
                S: supply at higher scales except local scale
                sp_amount_L: sharing principle (emission/population/area...) at smaller scale
                sp_amount_H: sharing principle (emission/population/area...) at larger scale
                '''
                S = SP_info[k][v]['public supply']
                sp_amount_H = SP_info[k][v][sp_name] 
                frac = frac * (sp_amount_L / sp_amount_H)
                allo_S += frac * S
                sp_amount_L = sp_amount_H
            self.supply[es] = allo_S + local_S



class LcaSystem:
    def __init__(self):
        self.processes = []


    def add_process(self, data, SP_info):

        for i in range(data.shape[0]): 
            '''
            1. generate Process for each row from the dataframe
            2. add each Process to the LcaSystem
            !!Todo
            decide the input data structure: dataframe or dictionary? whether to have a function to formatting the data
            '''
            df_proc = data.loc[[i]] # -> structure as info
            process = Process()
            process.build_proc(df_proc)
            process.cal_supply(df_proc, SP_info)
            self.processes.append(process) # a list contains all processes
        

    def AD_matrix(self):
        df_A = pd.read_csv('./data/tech_matrix.csv') # technology matrix
        df_D = pd.read_csv('./data/intv_matrix.csv') # intervention matrix
        mat_A = df_A.to_numpy()
        mat_D = df_D.to_numpy()
        self.tech_matrix = mat_A
        self.intv_matrix = mat_D
        self.ProcNum = mat_A.shape[1] # number of processes - column
        self.FlowNum = mat_D.shape[0] # number of elementary flows - row


    @staticmethod
    def diag_mat(m1, m2):
        if m1 == []:
            return m2
        else:
            TR = np.zeros((m1.shape[0], m2.shape[1])) # zero matrix on top right
            LL = np.zeros((m2.shape[0], m1.shape[1])) # zero matrix on lower left
            up = np.hstack((m1, TR))
            down = np.hstack((LL, m2))
            return np.vstack((up, down))


    def S_matrix(self):
        '''
        build S matrix from self.processes 
        for items in self.processes:
            ...
        !!! Todo:
        consider two cases: unit process and lca network
        '''
        old = []
        for p in self.processes():
            new = np.c_[list(p.supply().values())] # convert the list of supply to a vertical vector
            new = LcaSystem.diag_mat(old, new)
        self.supply_matrix = new


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
        self.AD_matrix()
        self.f_matrix()
        Ft = self.Ft
        S = self.supply_matrix
        A = self.tech_matrix
        D = self.intv_matrix
        me = np.zeros((S.shape[1], 1))
        C = np.zeros((self.ProcNum, S.shape[1]))
        I = np.eye(self.FlowNum)
        O = np.zeros((self.ProcNum, self.FlowNum))

        AD = np.vstack((A,D))
        OI = np.vstack((O, -I))
        FO = np.vstack((Ft, np.zeros(self.FlowNum, 1)))
        CS = np.vstack((C, S))
        LHS = np.hstack((AD, OI))
        RHS = FO - CS * me

        res = inv(LHS) * RHS

        return res
       

        
if __name__ == 'main':

    Pinfo = {
        'name': 'State',
        'location': 'Ohio',
        'type': 'Unit process',
        'ES local supply': None,
        'final demand': None,
        'scales': {
            'C sequestration': {
                'Country': 'United States',
                'World': 'World'
            }
        },
        'SP info': None
    }
 


