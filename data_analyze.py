#DFP project
#helper module to create data frame for interface
#Author: Yuwei Zhu

import pandas as pd

class Data(object):
    def __init__(self, data):
        self.data = data
    def feature_names(self):
        column = self.data.columns.tolist()
        return column
    def feature_index(self):
        col_index = {}
        column = self.data.columns.tolist()
        for i in range(len(column)):
            col_index[str(i)] = column[i]
        return col_index
    def get_value(self,column_name):
        value = self.data[column_name].tolist()
        return value
    def mean(self):
        city_mean = self.data.mean()
        return city_mean

class GroupData(object):
    def __init__(self, data):
        self.data = data.groupby(['Neighborhood']).mean().dropna()
    def feature_names(self):
        column = self.data.columns.tolist()
        return column
    def get_value(self,column_name):
        value = self.data[column_name].tolist()
        return value
    def get_index(self):
        col = []
        index = self.data.index
        for i in index:
            col += [i]
        return col
    def sort(self, column_name):
        self.data = self.data.sort_values(by = column_name, ascending=False)
        return
    def get_row_bar(self,name):
        #for bar chart, numbers in price, population and crime are much larger than others, here we drop them
        import copy
        drop_price = self.data.copy()
        del drop_price['Price']
        del drop_price['Population']
        del drop_price['Major Crime Report']
        row = drop_price.loc[name].tolist()
        feature = drop_price.columns.tolist()
        return row,feature
    def get_single_value_bar(self,col,row):
        value = self.data.loc[row][col]
        return value



