'''
Read user input daat from spreadsheet
constract proc_info as below
'''

    # proc_info = {
    #     'name': 'copper,cathode production',
    #     'type': '',
    #     'ES local supply': {
    #         'C sequestration': 200, # name of ES, will be used to search larger scale supply information in SP_info
    #         'Water provision': 3209
    #     },
    #     'final demand': 1000,
    #     'scales': { 
    #         'C sequestration': {
    #             'County': '1001',
    #             'World': 'World'
    #         },
    #         'water provision': {
    #             'Watershed': '03262000'
    #         }
    #     },
    #     'SP info':{ # local SP info for calculating allocation fractions
    #         'demand': {
    #             'C sequestration':78,
    #             'Water provision': 101
    #         },
    #         'population': {
    #             'C sequestration': 1209029,
    #             'water provision': None
    #         },
    #         'area': {
    #             'C sequestration': None,
    #             'water provision': None
    #         },
    #         'gdp': {
    #             'C sequestration': None,
    #             'water provision': None
    #         },
    #         'inverse gdp': {
    #             'C sequestration': None,
    #             'water provision': None
    #         }
    #     }
    # }


# Pinfo = {
#     'name': 'State',
#     'location': 'Ohio',
#     'type': 'Geo-unit process',
#     'ES local supply': None,
#     'final demand': None,
#     'scales': {
#         'C sequestration': {
#             'Country': 'United States',
#             'World': 'World'
#         }
#     },
#     'ES local demand': {
#         'C sequestration': 101,
#         'Water provision': 2347982
#     }
# }




procs = {
    '001':{
        'name': 'fertilizer',
        'location': 'xx st, Wisconsin', # address for checking whether user input info is correct, not directly used for LCA system
        'type': 'LCA',
        'ES local supply': {
            'C sequestration': 3200
        },
        'final demand': 0,
        'scales': {
            'C sequestration': {
                'State': 'Wisconsin',
                'World': 'World'
            }
        },
        'SP info': {
            'C sequestration': {
                'demand': 6400,
                'population': 100,
                'gdp': 50000,
                'inverse gdp': 1/50000,
                'area': 2000
            }
        }
    },
    '002':{
        'name': 'corn',
        'location': 'xx rd, Ohio',
        'type': 'LCA',
        'ES local supply': {
            'C sequestration': 5500
        },
        'final demand': 0,
        'scales': {
            'C sequestration': {
                'State': 'Ohio',
                'World': 'World'
            }
        },
        'SP info': {
            'C sequestration': {
                'demand': 11000,
                'population': 86,
                'gdp': 60000,
                'inverse gdp': 1/60000,
                'area': 2700
            }
        }
    },
    '003':{
        'name': 'ethanol',
        'location': 'xx rd, Ohio',
        'type':'LCA',
        'ES local supply': {
            'C sequestration': 2100
        },
        'final demand': 2000,
        'scales': {
            'State': 'Ohio',
            'World': 'World'
        },
        'SP info': {
            'C sequestration': {
                'demand': 4200,
                'population': 101,
                'gdp': 80000,
                'inverse gdp': 1/80000,
                'area': 3900
            }
        }
    }
}