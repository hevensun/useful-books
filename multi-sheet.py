#!/usr/bin/python
# -*- coding: utf-8 -*- 
import sys
import os
import xlrd
from xlrd import open_workbook
import re
from  datetime  import  *
from pymongo import Connection

reload(sys)  
sys.setdefaultencoding('utf8') 

#wb = open_workbook('5sheet.xlsx')
wb = open_workbook('data/test.xlsx')
for sheet in wb.sheets():
    print 'Sheet:',sheet.name, sheet.nrows, sheet.ncols
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        line = ""
        if row:
            for i in range(sheet.ncols):
                line = line + "|" + str(row[i])
        print rownum,":",line
    print
