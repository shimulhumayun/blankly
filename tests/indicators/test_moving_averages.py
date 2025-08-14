"""
    Indicator tests
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

from blankly.indicators import ema, hma, kaufman_adaptive_ma, macd, sma, trima, vwma, wma, zlema


def compare_equal(a, b):
    # compares two numpy arrays
    return np.array_equal(a, b)


class MovingAverages(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        data_path = Path("tests/config/test_data.p").resolve()
        with open(data_path, 'rb') as f:
            cls.data = pickle.load(f)

    def test_one_param_moving_averages(self):
        period = self.data['periods'][0]

        series = pd.Series(self.data['close'])

        ema_res = ema(self.data['close'], period)
        expected_ema = ta.ema(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(ema_res, expected_ema))

        wma_res = wma(self.data['close'], period)
        expected_wma = ta.wma(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(wma_res, expected_wma))

        zlema_res = zlema(self.data['close'], period)
        expected_zlema = ta.zlma(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(zlema_res, expected_zlema))

        sma_res = sma(self.data['close'], period)
        expected_sma = ta.sma(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(sma_res, expected_sma))

        hma_res = hma(self.data['close'], period)
        expected_hma = ta.hma(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(hma_res, expected_hma))

        kaufman_res = kaufman_adaptive_ma(self.data['close'], period)
        expected_kama = ta.kama(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(kaufman_res, expected_kama))

        trima_res = trima(self.data['close'], period)
        expected_trima = ta.trima(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(trima_res, expected_trima))

    def test_one_param_moving_averages_diff_period(self):
        period = self.data['periods'][1]

        series = pd.Series(self.data['close'])

        ema_res = ema(self.data['close'], period)
        expected_ema = ta.ema(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(ema_res, expected_ema))

        wma_res = wma(self.data['close'], period)
        expected_wma = ta.wma(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(wma_res, expected_wma))

        zlema_res = zlema(self.data['close'], period)
        expected_zlema = ta.zlma(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(zlema_res, expected_zlema))

        sma_res = sma(self.data['close'], period)
        expected_sma = ta.sma(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(sma_res, expected_sma))

        hma_res = hma(self.data['close'], period)
        expected_hma = ta.hma(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(hma_res, expected_hma))

        kaufman_res = kaufman_adaptive_ma(self.data['close'], period)
        expected_kama = ta.kama(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(kaufman_res, expected_kama))

        trima_res = trima(self.data['close'], period)
        expected_trima = ta.trima(series, length=period).dropna().to_numpy()
        self.assertTrue(compare_equal(trima_res, expected_trima))

    def test_macd(self):
        short_period = self.data['short_period']
        long_period = self.data['long_period']
        series = pd.Series(self.data['close'])
        for period in self.data['periods']:
            macd_res = macd(self.data['close'], short_period, long_period, period)
            df = ta.macd(series, fast=short_period, slow=long_period, signal=period)
            macd_col = f"MACD_{short_period}_{long_period}_{period}"
            macd_signal_col = f"MACDs_{short_period}_{long_period}_{period}"
            macd_hist_col = f"MACDh_{short_period}_{long_period}_{period}"
            expected = (
                df[macd_col].dropna().to_numpy(),
                df[macd_signal_col].dropna().to_numpy(),
                df[macd_hist_col].dropna().to_numpy()
            )
            for res_arr, exp_arr in zip(macd_res, expected):
                self.assertTrue(compare_equal(res_arr, exp_arr))

    def tests_vwma(self):
        volume = self.data['volume']
        series = pd.Series(self.data['close'])
        volume_series = pd.Series(volume)
        for period in self.data['periods']:
            vwma_res = vwma(self.data['close'], volume, period)
            expected_vwma = ta.vwma(series, volume_series, length=period).dropna().to_numpy()
            self.assertTrue(compare_equal(vwma_res, expected_vwma))
