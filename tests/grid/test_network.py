import os
import pandas as pd
from pandas.util.testing import assert_series_equal
from math import tan, acos
import numpy as np

from edisgo.grid.network import Network, TimeSeriesControl
from edisgo.data import import_data
from edisgo import EDisGo


class TestTimeSeriesControl:

    @classmethod
    def setup_class(self):
        """Setup default values"""
        parent_dirname = os.path.dirname(os.path.dirname(__file__))
        test_network_directory = os.path.join(parent_dirname, 'test_network')
        self.network = Network()
        import_data.import_ding0_grid(test_network_directory, self.network)

    def test_worst_case(self):
        """Test creation of worst case time series"""

        TimeSeriesControl(network=self.network, mode='worst-case')

        # check type
        assert isinstance(
            self.network.timeseries.generators_active_power, pd.DataFrame)
        assert isinstance(
            self.network.timeseries.generators_reactive_power, pd.DataFrame)
        assert isinstance(
            self.network.timeseries.loads_active_power, pd.DataFrame)
        assert isinstance(
            self.network.timeseries.loads_reactive_power, pd.DataFrame)

        # check shape
        number_of_timesteps = len(self.network.timeseries.timeindex)
        number_of_cols = len(self.network.generators_df.index)
        assert self.network.timeseries.generators_active_power.shape == (
            number_of_timesteps, number_of_cols)
        assert self.network.timeseries.generators_reactive_power.shape == (
            number_of_timesteps, number_of_cols)
        number_of_cols = len(self.network.loads_df.index)
        assert self.network.timeseries.loads_active_power.shape == (
            number_of_timesteps, number_of_cols)
        assert self.network.timeseries.loads_reactive_power.shape == (
            number_of_timesteps, number_of_cols)

        # value
        gen = 'Generator_1'  # gas, mv
        exp = pd.Series(data=[1 * 0.775, 0 * 0.775], name=gen,
                        index=self.network.timeseries.timeindex)
        assert_series_equal(
            self.network.timeseries.generators_active_power.loc[:, gen], exp)
        pf = -tan(acos(0.9))
        assert_series_equal(
            self.network.timeseries.generators_reactive_power.loc[:, gen],
            exp * pf)

        gen = 'GeneratorFluctuating_2'  # wind, mv
        exp = pd.Series(data=[1 * 2.3, 0 * 2.3], name=gen,
                        index=self.network.timeseries.timeindex)
        assert_series_equal(
            self.network.timeseries.generators_active_power.loc[:, gen], exp)
        pf = -tan(acos(0.9))
        assert_series_equal(
            self.network.timeseries.generators_reactive_power.loc[:, gen],
            exp * pf)

        gen = 'GeneratorFluctuating_3'  # solar, mv
        exp = pd.Series(data=[0.85 * 2.67, 0 * 2.67], name=gen,
                        index=self.network.timeseries.timeindex)
        assert_series_equal(
            self.network.timeseries.generators_active_power.loc[:, gen], exp)
        pf = -tan(acos(0.9))
        assert_series_equal(
            self.network.timeseries.generators_reactive_power.loc[:, gen],
            exp * pf)

        gen = 'GeneratorFluctuating_20'  # solar, lv
        exp = pd.Series(data=[0.85 * 0.005, 0 * 0.005], name=gen,
                        index=self.network.timeseries.timeindex)
        assert_series_equal(
            self.network.timeseries.generators_active_power.loc[:, gen], exp)
        pf = -tan(acos(0.95))
        assert_series_equal(
            self.network.timeseries.generators_reactive_power.loc[:, gen],
            exp * pf)

        load = 'Load_retail_MVGrid_1_Load_aggregated_retail_' \
               'MVGrid_1_1'  # retail, mv
        exp = pd.Series(data=[0.15 * 1520 * 0.0002404, 1.0 * 1520 * 0.0002404],
                        name=load, index=self.network.timeseries.timeindex)
        assert_series_equal(
            self.network.timeseries.loads_active_power.loc[:, load], exp,
            check_exact=False, check_dtype=False)
        pf = tan(acos(0.9))
        assert_series_equal(
            self.network.timeseries.loads_reactive_power.loc[:, load],
            exp * pf, check_exact=False, check_dtype=False)

        load = 'Load_agricultural_LVGrid_1_2'  # agricultural, lv
        exp = pd.Series(data=[0.1 * 514 * 0.00024036, 1.0 * 514 * 0.00024036],
                        name=load, index=self.network.timeseries.timeindex)
        assert_series_equal(
            self.network.timeseries.loads_active_power.loc[:, load], exp,
            check_exact=False, check_dtype=False)
        pf = tan(acos(0.95))
        assert_series_equal(
            self.network.timeseries.loads_reactive_power.loc[:, load],
            exp * pf, check_exact=False, check_dtype=False)

        load = 'Load_residential_LVGrid_3_3'  # residential, lv
        exp = pd.Series(data=[0.1 * 4.3 * 0.00021372, 1.0 * 4.3 * 0.00021372],
                        name=load, index=self.network.timeseries.timeindex)
        assert_series_equal(
            self.network.timeseries.loads_active_power.loc[:, load], exp,
            check_exact=False, check_dtype=False)
        pf = tan(acos(0.95))
        assert_series_equal(
            self.network.timeseries.loads_reactive_power.loc[:, load],
            exp * pf, check_exact=False, check_dtype=False)

        load = 'Load_industrial_LVGrid_6_1'  # industrial, lv
        exp = pd.Series(data=[0.1 * 580 * 0.000132, 1.0 * 580 * 0.000132],
                        name=load, index=self.network.timeseries.timeindex)
        assert_series_equal(
            self.network.timeseries.loads_active_power.loc[:, load], exp,
            check_exact=False, check_dtype=False)
        pf = tan(acos(0.95))
        assert_series_equal(
            self.network.timeseries.loads_reactive_power.loc[:, load],
            exp * pf, check_exact=False, check_dtype=False)

        load = 'Load_retail_LVGrid_9_14'  # industrial, lv
        exp = pd.Series(data=[0.1 * 143 * 0.0002404, 1.0 * 143 * 0.0002404],
                        name=load, index=self.network.timeseries.timeindex)
        assert_series_equal(
            self.network.timeseries.loads_active_power.loc[:, load], exp,
            check_exact=False, check_dtype=False)
        pf = tan(acos(0.95))
        assert_series_equal(
            self.network.timeseries.loads_reactive_power.loc[:, load],
            exp * pf, check_exact=False, check_dtype=False)

        # test when p_nom, type, etc. is missing
        # test for only feed-in or load case

    def test_reinforce(self):
        TimeSeriesControl(network=self.network, mode='worst-case')
        # ToDo: Remove and convert into csv table
        omega = 2 * np.pi * 50
        valid_lines = self.network.equipment_data['mv_lines'][
            self.network.equipment_data['mv_lines'].U_n ==
            self.network.buses_df.v_nom.iloc[0]]
        std_line = valid_lines.loc[valid_lines.I_max_th.idxmin()]
        self.network.lines_df[np.isnan(self.network.lines_df.x)] = self.network.lines_df[
            np.isnan(self.network.lines_df.x)].assign(num_parallel=1,
                  r=lambda _: _.length*std_line.loc['R_per_km'],
                  x=lambda _: _.length*std_line.loc['L_per_km']*omega/1e3,
                  s_nom=np.sqrt(3)*std_line.loc['I_max_th']*std_line.loc['U_n']/1e3,
                  type_info=std_line.name)

        timesteps = pd.date_range('1/1/1970', periods=1, freq='H')
        path = 'C:/Users/Anya.Heider/open_BEA/eDisGo/tests/test_network'
        edisgo = EDisGo(ding0_grid=path, worst_case_analysis='worst-case')
        pypsa_network = edisgo.network.to_pypsa(timesteps=timesteps)
