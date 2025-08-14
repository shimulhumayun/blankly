"""
    Oscillator wrappers
    Copyright (C) 2021 Brandon Fan

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

from typing import Any

import numpy as np
import pandas as pd

# pandas-ta expects the deprecated numpy.NaN alias.  Provide it for
# compatibility with NumPy 2.x before importing pandas_ta.
np.NaN = np.nan
import pandas_ta as ta

from blankly.indicators.utils import check_series


def rsi(data: Any, period: int = 14, round_rsi: bool = False, use_series=False) -> np.array:
    """ Implements RSI Indicator """
    if period >= len(data):
        return pd.Series() if use_series else []
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    rsi_values = ta.rsi(series, length=period).dropna()
    if round_rsi:
        rsi_values = np.round(rsi_values, 2)
    return rsi_values if use_series else rsi_values.to_numpy()


def aroon_oscillator(high_data: Any, low_data: Any, period=14, use_series=False):
    if check_series(high_data) or check_series(low_data):
        use_series = True
    high_series = pd.Series(high_data)
    low_series = pd.Series(low_data)
    aroon_df = ta.aroon(high_series, low_series, length=period)
    aroonsc = aroon_df[f"AROONOSC_{period}"].dropna()
    return aroonsc if use_series else aroonsc.to_numpy()


def chande_momentum_oscillator(data, period=14, use_series=False):
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    cmo = ta.cmo(series, length=period).dropna()
    return cmo if use_series else cmo.to_numpy()


def absolute_price_oscillator(data, short_period=12, long_period=26, use_series=False):
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    apo = ta.apo(series, fast=short_period, slow=long_period).dropna()
    return apo if use_series else apo.to_numpy()


def percentage_price_oscillator(data, short_period=12, long_period=26, use_series=False):
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    ppo = ta.ppo(series, fast=short_period, slow=long_period).dropna()
    return ppo if use_series else ppo.to_numpy()


def stochastic_oscillator(high_data, low_data, close_data, pct_k_period=14, pct_k_slowing_period=3, pct_d_period=3,
                          use_series=False):
    if check_series(high_data) or check_series(low_data) or check_series(close_data):
        use_series = True
    high_series = pd.Series(high_data)
    low_series = pd.Series(low_data)
    close_series = pd.Series(close_data)
    stoch_df = ta.stoch(high_series, low_series, close_series,
                        k=pct_k_period, d=pct_d_period, smooth_k=pct_k_slowing_period)
    pct_k = stoch_df[f"STOCHk_{pct_k_period}_{pct_d_period}_{pct_k_slowing_period}"].dropna()
    pct_d = stoch_df[f"STOCHd_{pct_k_period}_{pct_d_period}_{pct_k_slowing_period}"].dropna()
    if use_series:
        return pd.DataFrame({'pct_k': pct_k, 'pct_d': pct_d})
    return pct_k.to_numpy(), pct_d.to_numpy()


def stochastic_rsi(data, period=14, smooth_pct_k=3, smooth_pct_d=3):
    """ Calculates Stochoastic RSI Courteous of @lukazbinden
    :param data:
    :param period:
    :param smooth_pct_k:
    :param smooth_pct_d:
    :return:
    """
    # Calculate RSI
    rsi_values = rsi(data, period=period, round_rsi=False)

    # Calculate StochRSI
    rsi_values = pd.Series(rsi_values)
    stochrsi = (rsi_values - rsi_values.rolling(period).min()) / (
                rsi_values.rolling(period).max() - rsi_values.rolling(period).min())
    stochrsi_K = stochrsi.rolling(smooth_pct_k).mean()
    stochrsi_D = stochrsi_K.rolling(smooth_pct_d).mean()

    return round(rsi_values, 2), round(stochrsi_K * 100, 2), round(stochrsi_D * 100, 2)
