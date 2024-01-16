# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def calculate_rsi(data, period=14):
    # 计算价格变动
    delta = data['Close'].diff(1)

    # 分别计算上涨和下跌的价格变动
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # 计算平均增益和平均损失
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # 计算相对强弱指数（RSI）
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


import yfinance as yf

symbol = 'TSLA'

data = yf.download(symbol, start='2020-01-01', end='2021-01-015')
print(data)
data['RSI'] = calculate_rsi(data)

print(data[['Close', 'RSI']])
