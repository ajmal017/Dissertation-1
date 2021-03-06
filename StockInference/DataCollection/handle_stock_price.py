#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Dissertation
# File name: handle_stock_price
# Author: Mark Wang
# Date: 1/6/2016

import numpy

from StockInference.DataCollection.base_class import BaseClass
from StockInference.util.get_history_stock_price import get_all_data_about_stock
from StockInference.util.date_parser import get_ahead_date


class StockPriceHandler(BaseClass):
    def __init__(self, logger=None):
        BaseClass.__init__(self, logger)
        self.stock_price_min_list = None
        self.stock_price_max_list = None

    def handle_stock_price(self, data_period):

        if self.get_data_file_path():
            features = self.load_data_from_file("price_features.dat")
            if features is not None:
                return features

        if data_period == 1:
            stock_info = [i[1:] for i in self._stock_price]
            if self._price_type == self.STOCK_ADJUSTED_CLOSED:
                stock_info = map(lambda p: [p[0] * p[5] / p[3], p[1] * p[5] / p[3], p[2] * p[5] / p[3], p[5]],
                                 stock_info)
        else:
            stock_info = self.get_ahead_stock_price(data_period - 1)

        data_num = len(stock_info)
        if self.one_day_info:
            window_data = [stock_info[i:(i + data_period)] for i in range(data_num - data_period + 1)]
        else:
            window_data = [stock_info[i:(i + data_period)] for i in range(data_num - data_period)]
        max_price = []
        min_price = []
        close_avg_price = []
        open_avg_price = []
        for window in window_data:
            max_price.append(max([i[1] for i in window]))
            min_price.append(min([i[2] for i in window]))
            close_avg_price.append(numpy.mean([i[3] for i in window]))
            open_avg_price.append(numpy.mean([i[0] for i in window]))
        features = map(list, zip(open_avg_price, max_price, min_price, close_avg_price))
        self.save_data_to_file("price_features.dat", features)
        return features

        # def normalized_label(self, normalized_method, label_list, price_list):
        #     new_label_list = []
        #     for i, label in enumerate(label_list):
        #         new_label_list.append(normalized_method(label, price_list[i][1], price_list[i][2]))
        #     return new_label_list
        #
        # def normalize_stock_price(self, stock_price_list):
        #     temp_list = numpy.array(stock_price_list).astype(numpy.float)
        #     if not self.stock_price_max_list or not self.stock_price_min_list:
        #         self.stock_price_max_list = numpy.array([numpy.max(temp_list[:,i]) for i in range(4)])
        #         self.stock_price_min_list = numpy.array([numpy.min(temp_list[:,i]) for i in range(4)])
        #
        #     diff = self.stock_price_max_list - self.stock_price_min_list
        #     temp_list2 = map(lambda p: ((2 * p - self.stock_price_min_list - self.stock_price_max_list) / diff).tolist(),
        #                      temp_list)
        #     return temp_list2
        #
        # def de_normalize_stock_price(self, stock_price_list):
        #     diff = self.stock_price_max_list - self.stock_price_min_list
        #     stock_price_list = numpy.array(stock_price_list[:4])
        #     return stock_price_list * diff /2 + (self.stock_price_min_list + self.stock_price_max_list) / 2
