#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import codecs
import json
from operator import itemgetter
from pandas import *
import pandas as pd
from numpy import nan
import numpy as np


def get_table_range(rows, targets):
    bookmarks = []
    for target in targets:
        for i in range(0, len(rows)):
            if pd.notnull(rows[i]):
                if re.search(target, rows[i]):
                    bookmarks.append({"name": target, "position": i})
                    break
    return sorted(bookmarks, key=itemgetter('position'))

def clean_page_mark(df):
    rows = df_orgi[df_orgi.columns[0]]
    for i in range(0, len(rows)):
        if pd.notnull(rows[i]):
            if re.search(u'監察院公報', rows[i]):
                return df.drop(df.index[i-1:i+2])

df_orgi = pd.read_excel('data/tmp660b1.xlsx', 0)
#df_orgi = clean_page_mark(df_orgi)
first_column = df_orgi[df_orgi.columns[0]]
categories = [u'土地', u'建物', u'船舶', u'汽車', u'航空器', u'現金', u'存款', u'股票', u'債券', u'基金受益憑證', u'其他有價證券', u'珠寶、古董、字畫', u'保險', u'債權', u'債務', u'事業投資', u'備註']
print df_orgi[:50]
writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
bookmarks = get_table_range(first_column, categories)
for i in range(0, len(bookmarks) - 1):
    df = df_orgi[bookmarks[i]['position']:bookmarks[i+1]['position']].dropna(how='all')
    df.to_excel(writer, sheet_name=bookmarks[i]['name'])
writer.save()
