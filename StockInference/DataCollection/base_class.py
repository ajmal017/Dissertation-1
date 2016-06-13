#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Dissertation
# File name: base_class
# Author: Mark Wang
# Date: 1/6/2016

import datetime
import logging
import re
import os
import pickle

import pandas as pd

from StockInference.constant import Constants
from StockInference.util.date_parser import custom_business_day, get_ahead_date, is_holiday


class BaseClass(Constants):
    def __init__(self, logger=None):
        self._stock_price = []
        self._start_date = None
        self._end_date = None
        self._true_end_date = None
        self._date_list = None
        self._stock_symbol = None
        self._price_type = self.STOCK_CLOSE
        self._data_file_path = None
        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)
        else:
            self.logger = logger.getLogger(self.__class__.__name__)

    def get_start_date(self, date_type='str'):
        if date_type == 'str':
            return self._start_date
        else:
            date_list = self._start_date.split('-')
            date_list = map(int, date_list)
            return datetime.datetime(date_list[0], date_list[1], date_list[2])

    def get_end_date(self, date_type='str'):
        if date_type == 'str':
            return self._end_date
        else:
            date_list = self._end_date.split('-')
            date_list = map(int, date_list)
            return datetime.datetime(date_list[0], date_list[1], date_list[2])

    def get_true_end_date(self):
        return self._true_end_date

    def set_start_date(self, date):
        self.logger.debug("Set start date to {}".format(date))
        if is_holiday(date):
            self._start_date = get_ahead_date(date, -1)
        else:
            self._start_date = date

    def set_end_date(self, date):
        self.logger.debug("Set end date to {}".format(date))
        if is_holiday(date):
            self._end_date = get_ahead_date(date, 1)
        else:
            self._end_date = date
        self._true_end_date = get_ahead_date(self._end_date, 1)

    def get_date_list(self):
        if not self._date_list:
            self.generate_date_list()
        return self._date_list[:]

    def generate_date_list(self, start_date=None, end_date=None):
        if start_date is None:
            start_date = self._start_date.split('-')
        else:
            start_date = start_date.split('-')

        if end_date is None:
            end_date = self._end_date.split('-')
        else:
            end_date = end_date.split('-')

        start_date = map(int, start_date)
        end_date = map(int, end_date)
        start_date = pd.datetime(year=start_date[0], month=start_date[1], day=start_date[2])
        end_date = pd.datetime(year=end_date[0], month=end_date[1], day=end_date[2])
        self._date_list = []
        while start_date <= end_date:
            self._date_list.append(start_date.strftime("%Y-%m-%d"))
            start_date += custom_business_day

    def _merge_info(self, calculated_info, info_dict):

        # merge bond info into calculated list
        if info_dict is None:
            return calculated_info
        for i in calculated_info:
            if i[0] in info_dict:
                i.append(info_dict[i[0]])
            else:
                i.append(0)
        return calculated_info

    def get_data_file_path(self):
        return self._data_file_path

    def set_data_file_path(self, path):
        if path is not None:
            from_date = "".join(self._start_date.split('-'))
            to_date = "".join(self._end_date.split('-'))
            symbol = self._stock_symbol
            symbol = "".join(re.findall(r'\w+', symbol))
            data_folder = "{}_{}_{}".format(symbol, from_date, to_date)
            self._data_file_path = os.path.join(path, data_folder)
            if not os.path.isdir(self._data_file_path):
                os.makedirs(self._data_file_path)
            self.logger.debug("Data will be saved to {}".format(self._data_file_path))

    def load_data_from_file(self, file_name):
        if self._data_file_path:
            new_file_name = re.findall(r'[a-zA-Z0-9]+', file_name)
            if 'dat' in new_file_name:
                new_file_name.remove('dat')

            new_file_name = "{}.dat".format("_".join(new_file_name))

            file_path = os.path.join(self._data_file_path, self.get_price_type(), new_file_name)
            if os.path.isfile(file_path):
                self.logger.debug("Load data from {}".format(new_file_name))
                f = open(file_path)
                data = pickle.load(f)
                f.close()
            else:
                self.logger.warn("No such data, load nothing")
                data = None
        else:
            self.logger.warn("File path not set, load nothing")
            data = None
        return data

    def save_data_to_file(self, file_name, data):
        if self._data_file_path:
            new_file_name = re.findall(r'[a-zA-Z0-9]+', file_name)
            if 'dat' in new_file_name:
                new_file_name.remove('dat')

            new_file_name = "{}.dat".format("_".join(new_file_name))

            if not os.path.isdir(os.path.join(self._data_file_path, self.get_price_type())):
                os.makedirs(os.path.join(self._data_file_path, self.get_price_type()))
            save_path = os.path.join(self._data_file_path, self.get_price_type(), new_file_name)
            f = open(save_path, 'w')
            pickle.dump(data, f)
            self.logger.debug("Save data to {}".format(save_path))
            f.close()
        else:
            self.logger.warning("File path not set, save Nothing")

    def set_price_type(self, price_type=None):
        if price_type is None or price_type not in [self.STOCK_CLOSE, self.STOCK_OPEN, self.STOCK_ADJUSTED_CLOSED]:
            price_type = self.STOCK_CLOSE

        self.logger.debug("Set price type to {}".format(price_type))
        self._price_type = price_type

    def get_price_type(self):
        return self._price_type


if __name__ == "__main__":
    from data_collect import DataCollect

    dc = DataCollect("0001.HK", "2012-03-01", "2012-04-01")
    data = dc.fundamental_analysis([dc.US10Y_BOND, dc.US30Y_BOND, dc.HSI, dc.FXI, dc.IC, dc.IA])
