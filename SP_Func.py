import numpy as np

def sharing_principle(loc, nScales, SPinfo):

    def SP_CAL(list, principle, loc, SPri):
        d1 = SPri[list[0]][principle]  # nation
        d2 = SPri[list[1]][principle]  # world
        s1 = loc[list[0]]  # [n1, n2, n3 ...]
        s2 = loc[list[1]]  # [g1, g2, g3 ...]
        sp_lst = []
        for i in range(len(s1)):
            sp = d1.at[0, s1[i]] / d2.at[0, s2[i]]
            sp_lst.append(sp)
        return np.diag(sp_lst)

    def subset(l):
        lpairs = []
        for i in range(len(l) - 1):
            pair = [l[i], l[i + 1]]
            lpairs.append(pair)
        return lpairs

    lst = []
    SPrinciple = input('Sharing Principle (gdp, inverse of gdp, emission, area, population): ')
    for i in range(nScales+1):
        scale = input('Geo-scale ' + str(i) + '(local, county, state, nation, world): ')
        lst.append(scale)

    pairlist = subset(lst)
    SP_Matrix = []
    for ele in pairlist:
        SP_Matrix.append(SP_CAL(ele, SPrinciple, loc, SPinfo))
    return SP_Matrix
