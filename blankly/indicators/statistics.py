"""
    Statistics functions
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

# pandas-ta uses the deprecated numpy.NaN attribute; reintroduce it for
# compatibility with NumPy 2.x before importing the library.
np.NaN = np.nan
import pandas_ta as ta

from blankly.indicators.utils import check_series


def stddev_period(data, period=14, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    stddev = ta.stdev(series, length=period).dropna()
    return stddev if use_series else stddev.to_numpy()


def var_period(data, period=14, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    var = ta.variance(series, length=period).dropna()
    return var if use_series else var.to_numpy()


def stderr_period(data, period=14, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    stderr = series.rolling(period).sem().dropna()
    return stderr if use_series else stderr.to_numpy()


def min_period(data, period, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    minimum = series.rolling(period).min().dropna()
    return minimum if use_series else minimum.to_numpy()


def max_period(data, period, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    maximum = series.rolling(period).max().dropna()
    return maximum if use_series else maximum.to_numpy()


def sum_period(data, period, use_series=False) -> Any:
    if check_series(data):
        use_series = True
    series = pd.Series(data)
    total = series.rolling(period).sum().dropna()
    return total if use_series else total.to_numpy()
