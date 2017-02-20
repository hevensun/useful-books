#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
根据给定的字符串，生成部分匹配列表
"""
#
#
import sys
from  datetime import  *
from  time     import *
from pymongo   import Connection

def subStrGet(uStr, minLen, index=None):
    "对unicode字符串，获得从头开始的所有可能子串. 返回子串为utf-8编码"
    # minLen: 部分匹配串的起始最小长度
    # index: 在names数组中的下标。如果index!=None,则需要在结果中携带index    
    retVal = []
    length = len(uStr)

    for keyLen in range(minLen, length+1):
        key = uStr[0:keyLen].encode('utf-8')
        
        if index == None:
            retVal.append(key)
        else:
            retVal.append([key, index])
    
    return retVal
  
def cnGen(inputText, minLen=1, index=None):
    "生成从头开始匹配的字符串列表"
    # minLen: 部分匹配串的起始最小长度
    # index: 在names数组中的下标。如果index!=None,则输出中名称可能不同
    retVal = []
    uStr = inputText.decode('utf-8')  # convert to unicode

    retVal = subStrGet(uStr, minLen, index)
    return retVal            

def anyGen(inputText, index=None):
    "生成从任意位置开始匹配的字符串列表"
    # minLen: 部分匹配串的起始最小长度
    # index: 在names数组中的下标。如果index!=None,则输出中名称可能不同
    retVal = []
    uStr = inputText.decode('utf-8')  # convert to unicode
            
    length = len(uStr)
    for start in range(0, length):
        subStr = uStr[start:length]
        retVal = retVal + subStrGet(subStr, 1, index)

    return retVal
    
def read_file(file):
    """read input file to list"""
    file_object = open(file, "r")
    try:
        all_lines = file_object.readlines( )
    finally:
        file_object.close( )
    return all_lines

def index_to_db(key_index_dict, collection):
    """key/val to db"""
    table_list  =  []

    systime     = str(datetime.now()).split(".")[0]
    for k,v in key_index_dict.items():

        #get val's list
        resVal = set([])
        res = collection.find({"_id":k})
        if res.count() == 1:
            resVal_list = res[0]["val"].split("")
            #print resVal_list,v
            resVal_list =[i.encode("utf-8") for i in resVal_list]
            #print resVal_list,v

        one_row = {}
        one_row["_id"] = k
        one_row["val"] = "".join(list(v | set(resVal)))
        one_row["uptime"] = systime
        table_list.append(one_row)
        collection.remove({"_id":k})


    # update stored index
    collection.insert(table_list)


def main_process(file_list, collection):
    """main process"""
    key_index_dict = {}

    # read file to list
    for file in file_list:
        keywords = read_file(file)

        # process keywords
        for kw in keywords:
            kw = kw.strip()
            words_list = anyGen(kw)
            for word in words_list:
                if not key_index_dict.has_key(word):
                    key_index_dict[word] = set([])
                key_index_dict[word].add(kw)


    # store key_index_dict to MongoDB
    print "will update:",len(key_index_dict)
    index_to_db(key_index_dict, collection)


if __name__ == '__main__':

    try:
        #conn  = Connection('192.168.39.174', 27017)
        #conn  = Connection('112.33.2.66', 27017)
        conn  = Connection('10.101.196.19', 27017)
        collection = conn.kb.keywords
        main_process(sys.argv[1:], collection)
    except Exception,e:
        print str(e)


    exit(0)

    retList =  anyGen(("动感地带I"))
    print len(retList)
    print retList
    for i in retList:
        print i,repr(i)

    retList =  cnGen(("动感地带I"))
    print len(retList)
    print retList
    for i in retList:
        print i,repr(i)

