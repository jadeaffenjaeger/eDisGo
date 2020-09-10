import os
import pandas as pd
import numpy as np
import pytest
import shutil
from math import tan, acos

from edisgo import EDisGo
from edisgo.io.generators_import import oedb


class TestEDisGo:

    @classmethod
    def setup_class(self):
        self.edisgo = EDisGo(ding0_grid=pytest.ding0_test_network_3_path,
                    generator_scenario='nep2035',
                             worst_case_analysis='worst-case')
        self.timesteps = pd.date_range('1/1/1970', periods=2, freq='H')


    def test_some(self):
        wind_old = self.edisgo.topology.generators_df[self.edisgo.topology.generators_df['type']=='wind'].p_nom.sum()
        biomass_old = self.edisgo.topology.generators_df[self.edisgo.topology.generators_df['type']=='biomass'].p_nom.sum()

        p_target = {'wind' : 0.8, 'biomass' : 0.8}
        oedb(self.edisgo, p_target)

        wind_new = self.edisgo.topology.generators_df[self.edisgo.topology.generators_df['type']=='wind'].p_nom.sum()
        biomass_new = self.edisgo.topology.generators_df[self.edisgo.topology.generators_df['type']=='biomass'].p_nom.sum()

        assert wind_old * 0.8 == pytest.approx(wind_new)
        assert biomass_old * 0.8 == pytest.approx(biomass_new)
