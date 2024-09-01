#!/usr/bin/env python
#import genStats as gs
import numpy as np
import pandas as pd

import urllib.request as urllib2
from bs4 import BeautifulSoup, Tag

import sys

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

verbose = False


def parse_html_table(table):
    n_columns = 0
    n_rows = 0
    column_names = []

    # Find number of rows and columns
    # we also find the column titles if we can
    for row in table.find_all('tr'):

        # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows += 1
            if n_columns == 0:
                # Set the number of columns for our table
                n_columns = len(td_tags)

        # Handle column names if we find them
        th_tags = row.find_all('th')
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())

    if 'Invalid Date' in column_names:
        return pd.DataFrame(columns=column_names)

    # Safeguard on Column Titles
    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("Column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0, n_columns)
    df = pd.DataFrame(columns=columns,
                      index=range(0, n_rows))
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            df.iat[row_marker, column_marker] = column.get_text()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1

    # Convert to float if possible
    for col in df:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass

    print(df)
    return df


def getLTGrowthRate(stock):
    url = 'https://ca.finance.yahoo.com/quote/{s}/analysts?p={s}'.format(s=stock)
    #if verbose: print('Parsing', url)
    headers = {'User-Agent': user_agent}

    req = urllib2.Request(url, None, headers)  # The assembled request
    response = urllib2.urlopen(req)
    content = response.read()

    soup = BeautifulSoup(content, 'html.parser')
    LTGrowthRate = 0.0
    for table in soup.find_all('table'):
        df = parse_html_table(table)

        if df.columns.values[0] == 'Growth Estimates':
            stk = df[df['Growth Estimates'] == 'Next 5 Years (per annum)'][stock].values[0].replace('%', '')
            #ind = df[df['Growth Estimates'] == 'Next 5 Years (per annum)']['Industry'].values[0].replace('%', '')
            #sec = df[df['Growth Estimates'] == 'Next 5 Years (per annum)']['Sector'].values[0].replace('%', '')
            #sp500 = df[df['Growth Estimates'] == 'Next 5 Years (per annum)']['S&P 500'].values[0].replace('%', '')

            LTGrowthRate = stk if stk != 'N/A' else 5.0
            #if ind != 'N/A':
            #    LTGrowthRate = min(LTGrowthRate, np.float(ind))
            #if sec != 'N/A':
            #    LTGrowthRate = min(LTGrowthRate, np.float(sec))

    return LTGrowthRate

print(getLTGrowthRate("AMZN"))