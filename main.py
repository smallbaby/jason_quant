# -*- coding: utf-8 -*-

from datetime import datetime
import time
import alpaca_trade_api as tradeapi
import pandas as pd
import threading
from pytz import timezone
from config import *

pd.options.display.max_rows = 999
pd.set_option('display.max_columns', None)

tz = timezone('EST')
is_us_stock_market_open = False


def update_market_status():
    global is_us_stock_market_open

    # 设置美东时区
    us_eastern = timezone('America/New_York')

    # 获取当前时间
    current_time = datetime.now(us_eastern)

    # 设置美股开盘和闭市时间范围
    opening_time = datetime(current_time.year, current_time.month, current_time.day, 9, 0, 0, tzinfo=us_eastern)
    closing_time = datetime(current_time.year, current_time.month, current_time.day, 16, 0, 0, tzinfo=us_eastern)

    # 判断当前时间是否在开盘时间内
    if opening_time <= current_time <= closing_time:
        is_us_stock_market_open = True
    else:
        is_us_stock_market_open = False


def check_market_open():
    # 每隔一段时间检查一次
    while True:
        update_market_status()
        if is_us_stock_market_open:
            print("美股正在开盘中")
        else:
            print("美股闭市中, 今日操作整理中....")
            print("xxxxx")
            print("今日内容打印完毕，程序即将退出..")
            import sys
            sys.exit(0)

        # 等待一段时间后再次检查
        time.sleep(60)  # 等待60秒后再次检查


class Alpaca(object):

    def __init__(self):
        self.symbols = ["AAPL", "TSLA", "META", "TQQQ"]
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.URL = END_POINT
        self.api = tradeapi.REST(self.API_KEY, self.SECRET_KEY, self.URL)
        self.cash = self.api.get_account().cash
        print(f"连接成功，当前账户可用现金 {self.cash}")

    def symbol_select(self):
        """选股"""
        while True:
            bars = self.api.get_latest_bars(self.symbols)
            for symbol, bar in bars.items():
                print(f"\t当前标的{symbol} 当前时间{bar.t} 最高价{bar.h} 最低价{bar.l}")
                # if symbol == 'TSLA':
                #     self.api.submit_order("TSLA", 1, 'buy', 'market', 'day')
            time.sleep(10)

    def cash_manager(self):
        while True:
            self.cash = self.api.get_account().cash
            print(f"当前账户可用现金 {self.cash}")
            time.sleep(60)

    def position_manager(self):
        """仓位管理 60s查看一次"""
        while True:
            for position in self.api.list_positions():
                print(f"当前持仓{position.symbol} 持仓数量：{position.qty_available} 持仓价格:{position.avg_entry_price},当前市价:{position.current_price}, 盈亏:${position.unrealized_intraday_pl}")
            time.sleep(60)

    def check(self, symbol, quantity):
        position = self.api.get_position(symbol)
        print('check', position)
        if position and position.qty_available >= quantity:
            return True
        else:
            return False

    def order(self, symbol, quantity, action):
        """
        买卖
        :param symbol: 标的
        :param quantity: 数量
        :param action: buy or sell
        :return:
        """
        if self.check(symbol, quantity):
            pass
            #self.api.submit_order(symbol, )


def main():
    if is_us_stock_market_open:
        alpaca = Alpaca()
        threading.Thread(target=alpaca.symbol_select).start()
        threading.Thread(target=alpaca.position_manager).start()
        threading.Thread(target=alpaca.cash_manager).start()
    else:
        print("未开市..")


if __name__ == '__main__':
    threading.Thread(target=check_market_open).start()
    time.sleep(5)
    main()
