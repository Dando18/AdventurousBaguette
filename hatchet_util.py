'''
Daniel Nichols
March 2021
'''
import hatchet as ht
import numpy as np

def find_slowest_functions(gf, n_slowest=3):
    gf = gf.deepcopy()
    gf.drop_index_levels(function=np.sum)
    function_agg = gf.dataframe.groupby('name').sum()
    sorted_df = function_agg.sort_values(by=['time'], ascending=False)
    return sorted_df.index[:n_slowest].tolist()


def get_total_runtime(gf):
    gf = gf.deepcopy()
    gf.drop_index_levels(function=np.sum)
    function_agg = gf.dataframe.groupby('name').sum()
    return function_agg[function_agg.index.str.startswith('main')].iloc[0]['time (inc)']
    #return function_agg['time (inc)'].loc['main']