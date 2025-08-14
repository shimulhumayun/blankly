"""
    Statistics tests
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

from blankly.indicators import max_period, min_period, stddev_period, stderr_period, var_period


def compare_equal(a, b):
    # compares two numpy arrays
    return np.array_equal(a, b)


class Statistics(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        data_path = Path("tests/config/test_data.p").resolve()
        with open(data_path, 'rb') as f:
            cls.data = pickle.load(f)

    def test_one_param_moving_averages(self):
        period = self.data['periods'][0]

        series = pd.Series(self.data['close'])

        stddev_res = stddev_period(self.data['close'], period)
        expected_stddev = ta.stdev(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(stddev_res, expected_stddev))

        var_res = var_period(self.data['close'], period)
        expected_var = ta.variance(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(var_res, expected_var))

        stderr_res = stderr_period(self.data['close'], period)
        expected_stderr = series.rolling(period).sem().dropna().to_numpy()
        self.assertTrue(compare_equal(stderr_res, expected_stderr))

        min_res = min_period(self.data['close'], period)
        expected_min = series.rolling(period).min().dropna().to_numpy()
        self.assertTrue(compare_equal(min_res, expected_min))

        max_res = max_period(self.data['close'], period)
        expected_max = series.rolling(period).max().dropna().to_numpy()
        self.assertTrue(compare_equal(max_res, expected_max))

    def test_one_param_moving_averages_diff_period(self):
        period = self.data['periods'][1]

        series = pd.Series(self.data['close'])

        stddev_res = stddev_period(self.data['close'], period)
        expected_stddev = ta.stdev(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(stddev_res, expected_stddev))

        var_res = var_period(self.data['close'], period)
        expected_var = ta.variance(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(var_res, expected_var))

        stderr_res = stderr_period(self.data['close'], period)
        expected_stderr = series.rolling(period).sem().dropna().to_numpy()
        self.assertTrue(compare_equal(stderr_res, expected_stderr))

        min_res = min_period(self.data['close'], period)
        expected_min = series.rolling(period).min().dropna().to_numpy()
        self.assertTrue(compare_equal(min_res, expected_min))

        max_res = max_period(self.data['close'], period)
        expected_max = series.rolling(period).max().dropna().to_numpy()
        self.assertTrue(compare_equal(max_res, expected_max))
