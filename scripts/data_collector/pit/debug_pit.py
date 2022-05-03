import pandas as pd

import qlib
from qlib.data import D

if __name__ == '__main__':
    qlib.init()

    fields = [
        "P(Mean($$roewa_q, 1))",
        "P($$roewa_q)",
        "P(Mean($$roewa_q, 2))",
        "P(Ref($$roewa_q, 1))",
        "P((Ref($$roewa_q, 1) +$$roewa_q) / 2)",
        "P(TTM($$roewa_q, 1, 2))",
    ]
    instruments = ["sh600519"]

    #print(eval('Operators.P(Operators.Ref(Operators.PFeature("roewa_q"),1))'))
    # latest period = 201803

    # # 201604, 201701, 201702, 201703, 201704
    # data = D.features(instruments, ["P(TTM($$roewa_q, 3, 2))"], start_time="2019-01-02", end_time="2020-01-02", freq="day")
    # print(data.tail())

    # # 201703, 201704, 201801, 201802, 201803
    # data = D.features(instruments, ["P(TTM($$roewa_q, 0, 2))"], start_time="2019-01-02", end_time="2020-01-02", freq="day")
    # print(data.tail())

    # # 201702, 201703, 201704, 201801, 201802
    # data = D.features(instruments, ["P(TTM($$roewa_q, 1, 2))"], start_time="2019-01-02", end_time="2020-01-02", freq="day")
    # print(data.tail())

    # # 201603, 201604, 201701, 201702, 201703
    # data = D.features(instruments, ["P(TTM($$roewa_q, 4, 2))"], start_time="2019-01-02", end_time="2020-01-02", freq="day")
    # print(data.tail())

    # 201704
    data = D.features(instruments, ["P(LYR($$roewa_q, 3))"], start_time="2019-01-02", end_time="2020-01-02", freq="day")
    print(data.tail())

    # 201704
    data = D.features(instruments, ["P(LYR($$roewa_q, 0))"], start_time="2019-01-02", end_time="2020-01-02", freq="day")
    print(data.tail())

    # 201704
    data = D.features(instruments, ["P(LYR($$roewa_q, 1))"], start_time="2019-01-02", end_time="2020-01-02", freq="day")
    print(data.tail())

    # 201604
    data = D.features(instruments, ["P(LYR($$roewa_q, 4))"], start_time="2019-01-02", end_time="2020-01-02", freq="day")
    print(data.tail())
