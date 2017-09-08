from edisgo.grid.network import Network, Scenario, TimeSeries, Results
from edisgo.flex_opt import reinforce_grid
import os
import pickle
import pandas as pd
from ast import literal_eval
import numpy as np
import datetime

timeseries = TimeSeries()
scenario = Scenario(timeseries=timeseries)

import_network = True

if import_network:
    network = Network.import_from_ding0(
        os.path.join('data', 'ding0_grids_example.pkl'),
        id='Test grid',
        scenario=scenario
    )
    pickle.dump(network, open('test_network.pkl', 'wb'))
else:
    network = pickle.load(open('test_network.pkl', 'rb'))

# Do non-linear power flow analysis with PyPSA
# network.analyze(mode='mv')

# for now create results object
results.pfa_p['p0'] = pfa_edges['p0'].apply(
    lambda x: np.array(x)[0])
results.pfa_p = results.pfa_p.transpose()
results.pfa_p['time'] = datetime.date.today()
results.pfa_p = results.pfa_p.set_index('time')

results.pfa_q['q0'] = pfa_edges['q0'].apply(
    lambda x: np.array(x)[0])
results.pfa_q = results.pfa_q.transpose()
results.pfa_q['time'] = datetime.date.today()
results.pfa_q = results.pfa_q.set_index('time')

pfa_nodes = pd.read_csv('Exemplary_PyPSA_bus_results.csv', index_col=0,
                        converters={'v_mag_pu': literal_eval})
results.pfa_v_mag_pu['v_mag_pu'] = pfa_nodes['v_mag_pu'].apply(
    lambda x: np.array(x)[0])
results.pfa_v_mag_pu = results.pfa_v_mag_pu.transpose()
results.pfa_v_mag_pu['time'] = datetime.date.today()
results.pfa_v_mag_pu = results.pfa_v_mag_pu.set_index('time')

# Print LV station secondary side voltage levels returned by PFA
# print(network.results.v_res(
#     network.mv_grid.graph.nodes_by_attribute('lv_station'), 'lv'))

# Print voltage level of all nodes
# print(network.results.pfa_v_mag_pu)

# Print apparent power at lines
# print(network.results.s_res([_['line'] for _ in network.mv_grid.graph.graph_edges()]))

# Print voltage levels for all lines
# print(network.results.s_res())

# # MV generators
# gens = network.mv_grid.graph.nodes_by_attribute('generator')
# print('Generators in MV grid incl. aggregated generators from MV and LV')
# print('Type\tSubtype\tCapacity in kW')
# for gen in gens:
#     print("{type}\t{sub}\t{capacity}".format(
#         type=gen.type, sub=gen.subtype, capacity=gen.nominal_capacity))
# 
# # Load located in aggregated LAs
# print('\n\nAggregated load in LA adds up to\n')
# if network.mv_grid.graph.nodes_by_attribute('load'):
#     [print('\t{0}: {1} MWh'.format(
#         _,
#         network.mv_grid.graph.nodes_by_attribute('load')[0].consumption[_] / 1e3))
#         for _ in ['retail', 'industrial', 'agricultural', 'residential']]
# else:
#     print("O MWh")

reinforce_grid.reinforce_grid(network, results)

# liste aller lv grids
# [_ for _ in network.mv_grid.lv_grids]

# nx.draw_spectral(list(network.mv_grid.lv_grids)[0].graph)

# ToDo: Parameter bei Komponenten einführen mit dem man feststellen kann, ob die Komponente bereits in einer ersten Maßnahme verstärkt oder ausgebaut wurde
# ToDo: Abbruchkriterium einführen - Anzahl paralleler lines

