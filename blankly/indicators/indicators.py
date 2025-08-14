"""
    Tulipy wrappers
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

import numpy as np
import pandas as pd

# pandas-ta requires the deprecated numpy.NaN attribute.  Define it for
# compatibility with NumPy 2.x before importing pandas_ta.
np.NaN = np.nan
import pandas_ta as ta

from blankly.indicators.utils import check_series


def bbands(data, period=14, stddev=2):
    series = pd.Series(data)
    bands = ta.bbands(series, length=period, std=stddev)
    lower = bands[f"BBL_{period}_{float(stddev)}"].dropna().to_numpy()
    middle = bands[f"BBM_{period}_{float(stddev)}"].dropna().to_numpy()
    upper = bands[f"BBU_{period}_{float(stddev)}"].dropna().to_numpy()
    return lower, middle, upper


def wad(high_data, low_data, close_data, use_series=False):
    if check_series(high_data) or check_series(low_data) or check_series(close_data):
        use_series = True
    high = pd.Series(high_data)
    low = pd.Series(low_data)
    close = pd.Series(close_data)
    prev_close = close.shift(1)
    wad_calc = []
    for h, l, c, pc in zip(high, low, close, prev_close):
        if np.isnan(pc):
            wad_calc.append(0)
        elif c > pc:
            wad_calc.append(c - min(l, pc))
        elif c < pc:
            wad_calc.append(c - max(h, pc))
        else:
            wad_calc.append(0)
    wad_series = pd.Series(wad_calc).cumsum().dropna()
    return wad_series if use_series else wad_series.to_numpy()


def wilders(data, period=50, use_series=False):
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    wilders = ta.rma(series, length=period).dropna()
    return wilders if use_series else wilders.to_numpy()


def willr(high_data, low_data, close_data, period=50, use_series=False):
    if check_series(high_data) or check_series(low_data) or check_series(close_data):
        use_series = True
    high = pd.Series(high_data)
    low = pd.Series(low_data)
    close = pd.Series(close_data)
    willr = ta.willr(high, low, close, length=period).dropna()
    return willr if use_series else willr.to_numpy()


def true_range(high_data, low_data, close_data, use_series=False):
    if check_series(high_data) or check_series(low_data) or check_series(close_data):
        use_series = True
    high = pd.Series(high_data)
    low = pd.Series(low_data)
    close = pd.Series(close_data)
    tr = ta.true_range(high, low, close).dropna()
    return tr if use_series else tr.to_numpy()


def average_true_range(high_data, low_data, close_data, period=50, use_series=False):
    if check_series(high_data) or check_series(low_data) or check_series(close_data):
        use_series = True
    high = pd.Series(high_data)
    low = pd.Series(low_data)
    close = pd.Series(close_data)
    atr = ta.atr(high, low, close, length=period).dropna()
    return atr if use_series else atr.to_numpy()
