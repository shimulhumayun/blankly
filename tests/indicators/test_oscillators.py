"""
    Oscillator tests
    Copyright (C) 2021  Emerson Dove

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pickle
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

# pandas-ta requires numpy.NaN to exist in NumPy 2.x
np.NaN = np.nan
import pandas_ta as ta

from blankly.indicators import absolute_price_oscillator, aroon_oscillator, chande_momentum_oscillator, \
    percentage_price_oscillator, rsi, stochastic_oscillator


def compare_equal(a, b):
    # compares two numpy arrays
    return np.array_equal(a, b)


class Oscillators(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        data_path = Path("tests/config/test_data.p").resolve()
        with open(data_path, 'rb') as f:
            cls.data = pickle.load(f)

    def test_rsi(self):
        series = pd.Series(self.data['close'])
        for period in self.data['periods']:
            rsi_res = rsi(self.data['close'], period)
            expected = ta.rsi(series, length=period).dropna().to_numpy()
            self.assertTrue(compare_equal(rsi_res, expected))

    def test_aroon_oscillator(self):
        high = pd.Series(self.data['high'])
        low = pd.Series(self.data['low'])
        for period in self.data['periods']:
            aroon_res = aroon_oscillator(self.data['high'], self.data['low'], period)
            expected_df = ta.aroon(high, low, length=period)
            expected = expected_df[f"AROONOSC_{period}"].dropna().to_numpy()
            self.assertTrue(compare_equal(aroon_res, expected))

    def test_chande_momentum_oscillator(self):
        series = pd.Series(self.data['close'])
        for period in self.data['periods']:
            chande_res = chande_momentum_oscillator(self.data['close'], period)
            expected = ta.cmo(series, length=period).dropna().to_numpy()
            self.assertTrue(compare_equal(chande_res, expected))

    def test_absolute_price_oscillator(self):
        short_period = self.data['short_period']
        long_period = self.data['long_period']
        series = pd.Series(self.data['close'])
        res = absolute_price_oscillator(self.data['close'], short_period, long_period)
        expected = ta.apo(series, fast=short_period, slow=long_period).dropna().to_numpy()
        self.assertTrue(compare_equal(res, expected))

    def test_percentage_price_oscillator(self):
        short_period = self.data['short_period']
        long_period = self.data['long_period']
        series = pd.Series(self.data['close'])
        res = percentage_price_oscillator(self.data['close'], short_period, long_period)
        expected = ta.ppo(series, fast=short_period, slow=long_period).dropna().to_numpy()
        self.assertTrue(compare_equal(res, expected))

    def test_stochastic_oscillator(self):
        pct_k_period = self.data['pct_k_period']
        pct_k_slowing_period = self.data['pct_k_slowing_period']
        pct_d_period = self.data['pct_d_period']
        res = stochastic_oscillator(self.data['high'], self.data['low'], self.data['close'], pct_k_period,
                                    pct_k_slowing_period, pct_d_period)
        high = pd.Series(self.data['high'])
        low = pd.Series(self.data['low'])
        close = pd.Series(self.data['close'])
        stoch_df = ta.stoch(high, low, close, k=pct_k_period, d=pct_d_period, smooth_k=pct_k_slowing_period)
        pct_k = stoch_df[f"STOCHk_{pct_k_period}_{pct_d_period}_{pct_k_slowing_period}"].dropna().to_numpy()
        pct_d = stoch_df[f"STOCHd_{pct_k_period}_{pct_d_period}_{pct_k_slowing_period}"].dropna().to_numpy()
        expected = (pct_k, pct_d)
        for res_arr, exp_arr in zip(res, expected):
            self.assertTrue(compare_equal(res_arr, exp_arr))
