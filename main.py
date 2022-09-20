from ast import main
import pandas as pd
import numpy as np
# from numpy.linalg import inv
from scipy.linalg import lu_factor, lu_solve
import json


f = open('SP_info3.json')
SP_info = json.load(f)



class Process:
    def __init__(self, info):
        self.name = info['name'] # this is used for geo-unit process: 'county', 'state', 'country'...
        self.type = info['type'] # LCA or geo unit
        self.location = info['location'] # this is used for geo-unit process: fips for county, state name for states
        self.scales = info['scales']
        self.f = info['final demand']
        self.local_supply = info['ES local supply']
        self.sharingP = info['sharing principle method']
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
        # SP_meth = self.sharingP
        
        for es in ES_name:
            SP_meth = self.sharingP[es]

            if type == 'Geo-unit process':
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
                local_S = proc_info['ES local supply'][es]
                sp_amount_L = proc_info['SP info'][es][SP_meth]
            
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
                S = SP_info[k][v]['public supply'][es]
                if SP_meth == 'demand': 
                    sp_amount_H = SP_info[k][v][SP_meth][es]
                else:
                    sp_amount_H = SP_info[k][v][SP_meth]
                frac = frac * (sp_amount_L / sp_amount_H)
                allo_S += frac * S
                sp_amount_L = sp_amount_H
            self.supply[es] = allo_S + local_S



class LcaSystem:
    def __init__(self):
        self.processes = []


    def add_process(self, data, SP_info):
        
        for p in data.values():
            process = Process(p)
            process.cal_supply(p, SP_info)
            self.processes.append(process)
        

    def AD_matrix(self):
        mat_A = pd.read_csv('./user_input_data/tech_matrix.csv', index_col=0).values # technology matrix
        mat_D = pd.read_csv('./user_input_data/intv_matrix.csv', index_col=0).values # intervention matrix
        self.tech_matrix = mat_A
        self.intv_matrix = mat_D
        self.ProcNum = mat_A.shape[1] # number of processes - column
        self.FlowNum = mat_D.shape[0] # number of elementary flows - row


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


    def S_matrix(self):
        '''
        build S matrix from self.processes 
        for items in self.processes:
            ...
        !!! Todo:
        consider two cases: geo unit process and lca network
        '''
        old = np.array([]) # empty array
        for p in self.processes:
            new = np.c_[list(p.supply.values())] # convert the list of supply to a vertical vector
            old = LcaSystem.diag_mat(old, new)
        self.supply_matrix = old


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
        me = np.ones((S.shape[1], 1))
        C = np.zeros((self.ProcNum, S.shape[1]))
        I = np.eye(self.FlowNum)
        O = np.zeros((self.ProcNum, self.FlowNum))

        AD = np.vstack((A,D))
        OI = np.vstack((O, -I))
        FO = np.vstack((Ft, np.zeros((self.FlowNum, 1))))
        CS = np.vstack((C, S))
        LHS = np.hstack((AD, OI))
        RHS = FO - CS @ me

        lu, piv = lu_factor(LHS)
        res = lu_solve((lu, piv), RHS)
        # res = inv(LHS) @ RHS

        return res
       

if __name__ == '__main__':

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


    procs = {
        'process1':{
            'name': 'fertilizer production',
            'location': '100 SW st, Wisconsin', # address for checking whether user input info is correct, not directly used for LCA system
            'final demand': 0,
            'type': 'LCA',
            'scales': {
                'carbon sequestration': {
                    'State': 'Wisconsin',
                    'World': 'World'
                }
            },
            'SP info': {
                'carbon sequestration': {
                    'demand': 6400,
                    'population': 100,
                    'gdp': 50000,
                    'inverse gdp': 1/50000,
                    'area': 2000
                }
            },
            'sharing principle method': {
                'carbon sequestration': 'population'
            },
            'ES local supply': {
                'carbon sequestration': 3200
            }
        },
        'process2':{
            'name': 'corn farm',
            'location': '2800 NE Rd, Ohio',
            'final demand': 0,
            'type': 'LCA',
            'scales': {
                'carbon sequestration': {
                    'State': 'Ohio',
                    'World': 'World'
                }
            },
            'SP info': {
                'carbon sequestration': {
                    'demand': 11000,
                    'population': 86,
                    'gdp': 60000,
                    'inverse gdp': 1/60000,
                    'area': 2700
                }
            },
            'sharing principle method': {
                'carbon sequestration': 'population'
            },
            'ES local supply': {
                'carbon sequestration': 5500
            }
        },
        'process3':{
            'name': 'ethanol production',
            'location': '150 wood st, Ohio',
            'final demand': 2000,
            'type':'LCA',
            'scales': {
                'carbon sequestration': {
                    'State': 'Ohio',
                    'World': 'World'
                }
            },
            'SP info': {
                'carbon sequestration': {
                    'demand': 4200,
                    'population': 101,
                    'gdp': 80000,
                    'inverse gdp': 1/80000,
                    'area': 3900
                }
            },
            'sharing principle method': {
                'carbon sequestration': 'population'
            },
            'ES local supply': {
                'carbon sequestration': 2100
            }
        }
    }



    # ohio = Process(proc)
    # ohio.cal_supply(proc, SP_info)

    obj1 = LcaSystem()
    obj1.add_process(procs, SP_info)
    obj1.AD_matrix()
    obj1.S_matrix()
    obj1.f_matrix()

    res = obj1.tes_cal()


    print('done!')




