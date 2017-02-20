#!/usr/bin/python
# -*- coding: utf-8 -*- 
import sys
import os
import xlrd
import re
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import string
from  datetime  import  *
import urllib2

reload(sys)  
sys.setdefaultencoding('utf8') 

def get_icon(appName):
    """get app icon"""
    try:
        url  = "http://app.mi.com/search?keywords="+appName

        html = urllib2.urlopen(url).read()

        soup = BeautifulSoup(html)
        #print soup.findAll(['title'])
        print soup.findAll('ul', attrs={'class': 'applist'})[0]["a"]
    except Exception, tx:  
        print '%s' % (tx.message)  


def read_excel_table(fullName, outFile, crawler):
    transDict = {"1":"即时通讯",  "2":"阅读",      "3":"社交",     "4":"地图导航", "5":"视频",
            "6":"音乐",      "7":"应用商店",  "8":"手机游戏", "9":"网银支付", "10":"动漫",
            "11":"商务办公", "12":"下载",     "13":"即时通讯","14":"",        "15":"",
            "16":"投资理财", "17":"安全杀毒", "18":""}
    fileObj = ""
    try:
        wb = xlrd.open_workbook(fullName)
        fileObj = file(outFile, 'w')
    except Exception,e:
        print str(e)
        exit


    retList  =  []
    for sheet in wb.sheets():

        nrows = sheet.nrows 
        ncols = sheet.ncols 
        if nrows==0 or ncols==0:
            continue

        print "sheet name:",sheet.name,"nrows:", nrows, "ncols:", ncols

        matchNum = re.findall(r'^\d+', sheet.name)
        bigType  = matchNum[0]

        # get column name
        colnames =  sheet.row_values(0)

        content  = ""
        newCat   = ""
        iconName = ""
        if transDict.has_key(bigType):
            newCat = transDict[bigType]

        for rownum in range(1,nrows):
            row = sheet.row_values(rownum)
            if row and (len(row)==4):
                chsName   = str(row[1])
                engName   = str(row[2])
                smallType = str(row[3])
                iconName  = get_icon(chsName + " " + engName)
                content = bigType + "|" + smallType + "|" + chsName + "|" + newCat
                fileObj.write(content + "\n")

                print content
    fileObj.close()


if __name__=="__main__":
    try:
        #read_excel_table(sys.argv[1], "newType.txt", crawler)
        get_icon("麦咖啡  mcafee")
    except Exception,e:
        print str(e)
        exit


