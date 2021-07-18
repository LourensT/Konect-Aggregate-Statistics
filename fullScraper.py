from os import name
import pandas as pd
from xml.etree import ElementTree as ET
from pandas.io import html
import requests
import numpy as np

from html.parser import HTMLParser

class TableParser(HTMLParser):

    ran = False

    def __init__(self, html, table_length, verbose = False):
        # super call
        HTMLParser.__init__(self)
        self.verbose = verbose

        # initalize table
        self.table = [[0] * 3 for i in range(table_length + 1)]
        self.table[0][0] = "Code"
        self.table[0][2] = "Link"

        # set indices to starting position
        self.row_index = -1
        self.column_index = -1
        self.table_encountered = False

        #start
        self.feed(html)
        self.ran = True

    def handle_starttag(self, tag, attrs):
        # only read data if we're in the table
        if tag == 'table':
            self.table_encountered = not self.table_encountered
            return

        if tag == 'tr': #we only have starting tags for each table-row, so we move pointer at start
            self.row_index += 1
            self.column_index = -1
            if self.verbose:
                print("ROW FINISHED:", self.row_index-1)
        if tag == 'td': #we only have starting tags for each table-field, so we move pointer at start
            self.column_index += 1
            if self.verbose:
                print("in cell  :(" + str(self.row_index) + ", " + str(self.column_index)+ ")")

        if self.table_encountered:
            if self.verbose:
                print("Start tag:", tag)
            for attr in attrs:
                if attr[0] == 'href' and self.column_index == 1:
                    self.table[self.row_index][self.column_index+1] = attr[1]       #column corrected to hold place for the Data
                    if self.verbose:
                        print("     attr:", attr)

    def handle_data(self, data):
        if self.verbose:
            print("Data in cell  :(" + str(self.row_index) + ", " + str(self.column_index)+ ")")
        if self.table_encountered and self.column_index < 2:
            self.table[self.row_index][self.column_index] = data
            if self.verbose:
                print("Adding data    :", data)
        else:
            if self.verbose:
                print("Not adding data:", data)

    def getTableAsDataFrame(self):
        df = pd.DataFrame.from_records(self.table)
        header = df.iloc[0]
        df = df[1:]
        df.columns = header
        return df

attributes_of_interest = []
url = 'http://konect.cc/networks/'
r = requests.get(url).text

tableParser = TableParser(r, 1326)
df = tableParser.getTableAsDataFrame().to_csv("try.csv")