from os import name
import pandas as pd
from xml.etree import ElementTree as ET
from pandas.io import html
import requests
import numpy as np

from html.parser import HTMLParser

import unicodedata

class TableParser(HTMLParser):

    ran = False
    BASE_URL = "http://konect.cc/networks/"

    def __init__(self,  verbose = False):
        HTMLParser.__init__(self)
        self.verbose = verbose

    def getScaffoldTable(self, html, table_length):
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

        self.all_networks = {}
        # set as df
        for network in self.table[1:]:
            self.all_networks[network[0]] = {"Name" : network[1], "URL" : network[2]}


    '''
    Scrapes both the given statistics and the attributes for all the networks. 

    @param: statistics: optionally provide a list of the statistics you want to scrape
    @param: first: optionally make the scraping stop after a given number of networks. For debugging mostly.
    '''
    def scrapeStatistics(self, statistics=None, first=None):

        count = 0

        for code, info in self.all_networks.items():

            if not first or count < first:
                print('Processing network: ', code)

                url = self.BASE_URL + info['URL']
                dfs =  pd.read_html(url)
                df_description = dfs[0]
                df_stats = dfs[1]

                info['Attributes'] = self.getAttributesOfNetwork(df_description)
                # union dictionaries
                stats = self.getStatisticsOfNetwork(df_stats, statistics=statistics)
                self.all_networks[code] = {**info, **stats}

                count += 1

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

    def getAttributesOfNetwork(self, df):
        attributes = []

        fields = df[df[0].isin(['Network format', 'Edge type'])][2]
        for field in fields:
            for attr in field.split(", "):
                attributes.append(attr)
        
        return attributes

    '''
    If statistics is left to be None all statistics are processed
    '''
    def getStatisticsOfNetwork(self, df, statistics=None):
        
        '''
        Helps with processing the numerical values
        '''
        def convert_to_float(x):
            x_new = unicodedata.normalize("NFKD", x)
            x_new = x_new.replace(' ', '')
            x_new = x_new.replace('−', '-') 

            # handle scientific notation
            if '10-' in x_new: 
                decimals = float(x_new.split('10-')[0][:-1])
                factor =  int(x_new.split('10-')[1])
                converted = decimals * 10**(-1*factor)
                return converted
            else:
                converted = float(x_new)
                return converted

        networkStatistics = {}

        for row in df.iterrows():
            if not statistics or row[1][0] in statistics:
                try:
                    statistic_numeric = int(row[1][2])
                except ValueError:
                    try:
                        statistic_numeric = convert_to_float(row[1][2])
                    except ValueError:
                        print("ValueError while numerically parsing {} for statistic{} , proceeding to save as string".format(row[1][2], row[1][0]))
                        statistic_numeric = row[1][2]

                assert (row[1][0] not in networkStatistics), "Statistic{} (with value {}) is a duplicate!".format(row[1][2], row[1][0])

                networkStatistics[row[1][0]] = statistic_numeric

        return networkStatistics

    def saveAsCSV(self, fp):
        pd.DataFrame.from_dict(self.all_networks, orient="index").to_csv(fp)


if __name__ == "__main__":
    url = 'http://konect.cc/networks/'
    r = requests.get(url).text

    tableParser = TableParser(verbose=False)
    tableParser.getScaffoldTable(r, 1326)
    tableParser.scrapeStatistics()
    tableParser.saveAsCSV('dataset.csv')