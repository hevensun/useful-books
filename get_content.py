#!/usr/bin/python
# -*- coding: utf-8 -*- 
import sys
import os
import xlrd
import re
from  datetime  import  *
from pymongo import Connection

reload(sys)  
sys.setdefaultencoding('utf8') 

#def read_excel_table(fullName, province, path, pathName):
def read_excel_table(fullName, subfullName, collection):
    try:
        wb = xlrd.open_workbook(fullName)
    except Exception,e:
        print str(e)
        exit

    # get province/path/name 
    # 业务类__基础服务__账务服务__发票__福建.xlsx
    fileName,ext = os.path.splitext(os.path.basename(fullName))
    sections = fileName.split("__")
    province = sections[-1]
    name     = sections[-2]
    type     = sections[0]
    path     = "/".join(sections[1:-2])
    print fileName,province,name,type,path
    collection.remove({"path":path, "name":name, "type":type})

    retList  =  []
    for sheet in wb.sheets():

        nrows = sheet.nrows 
        ncols = sheet.ncols 
        if ncols >10:
            ncols = 10
        if nrows==0 or ncols==0:
            continue

        print "table name:", fullName
        print "sheet name:",sheet.name,"nrows:", nrows, "ncols:", ncols
        
        # get column name
        indexList = []
        colnames =  sheet.row_values(0)
        for i in range(len(colnames)):
            if colnames[i] == "索引":
                indexList.append(i)

        systime     = datetime.now()

        oneSheet  =  {}
        content   =  ""
        title     =  ""
        for rownum in range(1,nrows):
            row = sheet.row_values(rownum)
            if row:
                for i in range(ncols) :
                    if not (i in indexList):
                        content = content + " " + str(row[i])
                        #print content
                
                if rownum == 1:
                    title = content

        #print "start assign data:"
        oneSheet["content"]   = content
        oneSheet["province"]  = province
        oneSheet["title"]     = title
        oneSheet["path"]      = path
        oneSheet["_id"]       = subfullName + "#" + sheet.name
        #print len(oneSheet)
        #print oneSheet
        retList.append(oneSheet)
        
        collection.remove({"_id":subfullName})
        #print retList

    return retList

def insert_into_db(mydb, collection, tableList):
    """insert data to db's table"""

    collection.insert(tableList)


def main(dirList, mydb, collection):
    """process data"""
    
    print dirList
    
    for root in dirList:
        if os.path.isdir(root):
            dirs  = os.listdir(root)
            for dir in dirs:
                subdir = root + "/" + dir
                if os.path.isdir(subdir):

                    files = os.listdir(subdir)
                    #print subdir
                    #print files
                    for fileName in files:            
                        #print fileName
                        if not os.path.isfile(subdir + '/' + fileName):
                            continue

                        if not fileName.endswith(".xlsx"):
                            continue

                        fullName = subdir + '/' + fileName
                        subfullName = dir + '/' + fileName

                        print fileName
                        try:
                            tableList = read_excel_table(fullName, subfullName, collection)
                            #print tableList

                            if len(tableList)>0:
                                insert_into_db(mydb, collection, tableList)
                        except Exception,e:
                            print str(e)
                            continue


if __name__=="__main__":

    try:
        conn  = Connection('192.168.39.174', 27017)
        #conn  = Connection('112.33.2.66', 27017)
        mydb  = conn.kb
        collection = mydb.url_table
        main(sys.argv[1:], mydb, collection)
    except Exception,e:
        print str(e)

