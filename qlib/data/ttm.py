# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.


from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd

from qlib.data.ops import Rolling
from ..log import get_module_logger

class TTM(Rolling):
    """Feature Reference

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        N = 0, retrieve the first data; N > 0, retrieve data of N periods ago; N < 0, future data
    type : int
        type = 0, 资产负债表 ; type = 1 利润表或现金流量表

    Returns
    ----------
    Expression
        a feature instance with target reference
    """

    def __init__(self, feature, N, type=1):
        super(TTM, self).__init__(feature, N, "ttm")
        self.type = type

    def _load_internal(self, instrument, start_index, end_index, *args):
        # start_index = ttm最早需要查询的period
        # end_index = 0
        series = self.feature.load(instrument, start_index, end_index, *args)
        # N = 0, return first day
        if series.empty:
            return series  # Pandas bug, see: https://github.com/pandas-dev/pandas/issues/21049
        else:
            #series = series.shift(self.N)  # copy
            series = series.iloc[:len(series) - self.N]  # copy
        # 在series.iloc[-1]上聚合操作TTM

        # (TODO)缺失值处理
        # TTM处理，参考https://www.cnblogs.com/the-wolf-sky/p/10562783.html的处理流程
        # 1. 对于资产负债表来说，由于其为时点数据，如果要计算其科目TTM数据
        # 常见有三种算法：1）当前最新数据；2）最近四个报告期平均值；3）当前最新报告期和其同比报告期的平均值
        # ricequant用的是第二种方法处理
        if self.type == 1:
            series.iloc[-1] = series.mean()
        #
        # 2. 对于利润表和现金流量表来说，如果最新报告期为年报，则TTM数据即为年报数据；
        # 如果是其他报告期，则TTM数据等于当前最新报告期数据，加上上年年报数据，减去上年同比报告期数据；
        # 如果上年年报或同比报告期不存在，可以使用年化算法，即当前最新报告期数据乘以年化系数，
        # 一季报、中报和三季报的年化系数分别为4、2、4/3
        elif self.type == 2:
            year = series.index[-1] // 100
            quarter = series.index[-1] % 100
            if quarter == 4:
                # 如果是年报，TTM数据就是当前最新报告期的数据
                pass
            else:
                # 非年报需要加上上年年报数据，再减去去年同比报告期数据
                # 如果不存在，则用最新报告期进行年化处理
                lyr_qurater = (year - 1) * 100 + quarter
                last_year = (year - 1) * 100 + 4
                if pd.isna(series.loc[last_year]) or pd.isna(series.loc[lyr_qurater]):
                    # 年化处理
                    if quarter == 1:
                        series.iloc[-1] *= 4.
                    elif quarter == 2:
                        series.iloc[-1] *= 2.
                    elif quarter == 3:
                        series.iloc[-1] *= (4. / 3.)
                else:
                    series.iloc[-1] += (series.loc[last_year] - series.loc[lyr_qurater])
        else:
            # (TOOD) log and raise exception
            raise Exception('not supported type.')
        return series

    def get_longest_back_rolling(self):
        if self.N == 0:
            return np.inf
        return self.feature.get_longest_back_rolling() + self.N

    def get_extended_window_size(self):
        # 最多向前回溯4个季度数据，覆盖上一期年报和同比季度的报告期
        return self.N + 4, 0
        # if self.N == 0:
        #     get_module_logger(self.__class__.__name__).warning("The Ref(ATTR, 0) will not be accurately calculated")
        #     return self.feature.get_extended_window_size()
        # else:
        #     lft_etd, rght_etd = self.feature.get_extended_window_size()
        #     lft_etd = max(lft_etd + self.N, lft_etd)
        #     rght_etd = max(rght_etd - self.N, rght_etd)
        #     return lft_etd, rght_etd


class LYR(Rolling):
    """Feature Reference

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        N = 0, retrieve the first data; N > 0, retrieve data of N periods ago; N < 0, future data

    Returns
    ----------
    Expression
        a feature instance with target reference
    """

    def __init__(self, feature, N):
        super(LYR, self).__init__(feature, N, "lyr")

    def _load_internal(self, instrument, start_index, end_index, *args):
        # start_index = lyr最早需要查询的period
        # end_index = 0
        series = self.feature.load(instrument, start_index, end_index, *args)
        # N = 0, return first day
        if series.empty:
            return series  # Pandas bug, see: https://github.com/pandas-dev/pandas/issues/21049
        else:
            #series = series.shift(self.N)  # copy
            series = series.iloc[:len(series) - self.N]  # copy
        # 将最近一期年报放入series.iloc[-1]
        year = series.index[-1] // 100
        quarter = series.index[-1] % 100
        if quarter < 4:
            series.iloc[-1] = series.loc[(year - 1) * 100 + 4]
        return series

    def get_longest_back_rolling(self):
        if self.N == 0:
            return np.inf
        return self.feature.get_longest_back_rolling() + self.N

    def get_extended_window_size(self):
        # 最多向前回溯3个季度数据，覆盖上一期年报
        return self.N + 3, 0
        # if self.N == 0:
        #     get_module_logger(self.__class__.__name__).warning("The Ref(ATTR, 0) will not be accurately calculated")
        #     return self.feature.get_extended_window_size()
        # else:
        #     lft_etd, rght_etd = self.feature.get_extended_window_size()
        #     lft_etd = max(lft_etd + self.N, lft_etd)
        #     rght_etd = max(rght_etd - self.N, rght_etd)
        #     return lft_etd, rght_etd