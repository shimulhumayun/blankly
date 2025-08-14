"""
    Moving average function utils
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

# pandas-ta relies on the deprecated numpy.NaN alias which was removed in
# NumPy 2.0.  Create that alias before importing the library so that the
# import works on modern NumPy versions.
np.NaN = np.nan
import pandas_ta as ta

from blankly.indicators.utils import check_series


def ema(data: Any, period: int = 50, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    ema = ta.ema(series, length=period).dropna()
    return ema if use_series else ema.to_numpy()


def vwma(data: Any, volume_data: Any, period: int = 50, use_series=False) -> Any:
    if check_series(data):
        use_series = True

    price = pd.Series(data)
    volume = pd.Series(volume_data).astype(float)

    vwma = ta.vwma(price, volume, length=period).dropna()
    return vwma if use_series else vwma.to_numpy()


def wma(data: Any, period: int = 50, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    wma = ta.wma(series, length=period).dropna()
    return wma if use_series else wma.to_numpy()


def zlema(data: Any, period: int = 50, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    zlema = ta.zlma(series, length=period).dropna()
    return zlema if use_series else zlema.to_numpy()


def sma(data: Any, period: int = 50, use_series=False) -> Any:
    """
    Finding the moving average of a dataset
    Args:
        data: (list) A list containing the data you want to find the moving average of
        period: (int) How far each average set should be
    """
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    sma = ta.sma(series, length=period).dropna()
    return sma if use_series else sma.to_numpy()


def hma(data: Any, period: int = 50, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    hma = ta.hma(series, length=period).dropna()
    return hma if use_series else hma.to_numpy()


def kaufman_adaptive_ma(data: Any, period: int = 50, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    kama = ta.kama(series, length=period).dropna()
    return kama if use_series else kama.to_numpy()


def trima(data: Any, period: int = 50, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    trima = ta.trima(series, length=period).dropna()
    return trima if use_series else trima.to_numpy()


def macd(data: Any, short_period: int = 12, long_period: int = 26, signal_period: int = 9, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    df = ta.macd(series, fast=short_period, slow=long_period, signal=signal_period)
    macd_col = f"MACD_{short_period}_{long_period}_{signal_period}"
    macd_signal_col = f"MACDs_{short_period}_{long_period}_{signal_period}"
    macd_hist_col = f"MACDh_{short_period}_{long_period}_{signal_period}"
    macd = df[macd_col].dropna()
    macd_signal = df[macd_signal_col].dropna()
    macd_hist = df[macd_hist_col].dropna()
    if use_series:
        return pd.DataFrame({
            'macd': macd,
            'macd_signal': macd_signal,
            'macd_histogram': macd_hist
        })
    return macd.to_numpy(), macd_signal.to_numpy(), macd_hist.to_numpy()
