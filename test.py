# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/7/24 11:33
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : test.py
# @Software: PyCharm
import sqlite3
import os
import time
import datetime

data={'username':'幼稚园园长3','email':'1796031sda384@qq.com','mess':'testtesttest3'}
for k in data.items():
    print(k[1])


def createtable(path):
    sql = '''
       create table msgs
       ( id integer primary key autoincrement,
       username text,
       email text,
       msg text
       )
       '''
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()



def saveMsg(msglist,dbpath):
    if os.path.exists('msg.db')==True:
        conn = sqlite3.connect(dbpath)
        cur=conn.cursor()
        data=[]
        for ii in msglist.items():
            data.append(ii[1])
        for i in range(len(data)):
            data[i]='"'+data[i]+'"'
        sql='''
                insert into msgs (username,email,msg)
                values(%s)
                '''%",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
        conn.close()
        print("1")
    else:
        createtable(dbpath)
        conn = sqlite3.connect(dbpath)
        cur=conn.cursor()
        data=[]
        for ii in msglist.items():
            data.append(ii[1])
        for i in range(len(data)):
            data[i]='"'+data[i]+'"'
        sql='''
                insert into msgs (username,email,msg)
                values(%s)
                '''%",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
        conn.close()
        print("2")

#读取留言
def showmsg():
    #创建空列表储存内容
    datalist = []
    #连接数据库
    conn = sqlite3.connect("msg.db")
    cur = conn.cursor()
    sql = '''
    select * from msgs
    '''
    data = cur.execute(sql)
    #遍历加列列表
    for item in data:
        datalist.append(item)
    conn.commit()
    cur.close()
    conn.commit()
    conn.close()
    smsgdata=data
    return smsgdata

now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(now)
print(datetime)