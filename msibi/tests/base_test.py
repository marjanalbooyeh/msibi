import os
import pytest

import numpy as np

from msibi import Angle, Bond, Pair, State


dr = 0.1 / 6.0
r = np.arange(0, 2.5 + dr, dr)
k_B = 1.9872041e-3  # kcal/mol-K
T = 298.0  # K
test_assets = os.path.join(os.path.dirname(__file__), "assets")


class BaseTest:
    @pytest.fixture
    def state0(self, tmp_path):
        return self.init_state(0, tmp_path)

    @pytest.fixture
    def state1(self, tmp_path):
        return self.init_state(1, tmp_path)

    @pytest.fixture
    def pairs(self):
        pair0 = Pair("0", "0")
        pair0.set_table_potential(
                epsilon=1, sigma=1, r_min=0, r_max=2.5, n_points=len(r)
        )
        pair1 = Pair("1", "1")
        pair1.set_table_potential(
                epsilon=1, sigma=1, r_min=0, r_max=2.5, n_points=len(r)
        )
        pair2 = Pair("2", "2")
        pair2.set_table_potential(
                epsilon=1, sigma=1, r_min=0, r_max=2.5, n_points=len(r)
        )
        pair01 = Pair("0", "1")
        pair01.set_table_potential(
                epsilon=1, sigma=1, r_min=0, r_max=2.5, n_points=len(r)
        )
        pair02 = Pair("0", "2")
        pair02.set_table_potential(
                epsilon=1, sigma=1, r_min=0, r_max=2.5, n_points=len(r)
        )
        pair12 = Pair("1", "2")
        pair12.set_table_potential(
                epsilon=1, sigma=1, r_min=0, r_max=2.5, n_points=len(r)
        )
        return [pair0, pair1, pair2, pair01, pair02, pair12]
    
    @pytest.fixture
    def bond(self):
        bond = Bond("0", "1")
        bond.set_quadratic(l0=1, k4=1, k3=1, k2=1, l_min=0, l_max=2)
        return bond

    @pytest.fixture
    def angle(self):
        angle = Angle("0", "1", "2")
        angle.set_harmonic(k=1, theta0=1)
        angle.set_quadratic(theta0=1, k4=1, k3=1, k2=1)
        return angle

    @pytest.fixture
    def rdf0(self):
        return self.get_rdf(0)

    @pytest.fixture
    def rdf1(self):
        return self.get_rdf(1)

    def get_rdf(self, state_n):
        return np.loadtxt(os.path.join(test_assets, f"target-rdf{state_n}.txt"))

    def init_state(self, state_n, tmp_path):
        traj_filename = os.path.join(test_assets, f"query{state_n}.gsd")
        state = State(
            name=f"state{state_n}",
            kT=T,
            max_frames=5,
            alpha=0.5,
            traj_file=traj_filename,
            _dir=tmp_path
        )
        return state
