# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/7/9 16:31
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : urllibtest.py
# @Software: PyCharm

#本文件为爬虫板块，从网页爬取数据并写入数据库

from bs4 import BeautifulSoup       #网页解析，获取数据
import urllib.request
import xlwt         #excel操作
import re           #正则，匹配文字
import sqlite3      #数据库操作


def main():
    baseurl="https://movie.douban.com/top250?start="
    datalist=getData(baseurl) #获取数据
    path = ".\\" #存储路径
    dbpath = "movie.db"
    saveData2(datalist,dbpath)
    # saveData(datalist,path) #存储数据


def askUrl(url):  #请求网页 返回html
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWe bKit/537.36 (KHTML, like Gecko) Chrome/93.0.4544.0 Safari/537.36 Edg/93.0.933.1",
    }#头部信息用户代理
    request = urllib.request.Request(url,headers=headers)  #对象
    try:
        response = urllib.request.urlopen(request)  #获取
        html = response.read().decode("utf-8")
    except Exception as err:
        print("出现错误",err)
    return html

findLink=re.compile(r'<a href="(.*?)">')
findImg=re.compile(r'<img.*src="(.*?)"',re.S) #re.S忽略换行符
fingTitle=re.compile(r'<span class="title">(.*?)</span>')
fingRating=re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
findCNumber=re.compile(r'<span>(\d*)人评价</span>')
findDics=re.compile(r'<span class="inq">(.*?)</span>',re.S)
findInfo=re.compile(r'<p class="">(.*?)</p>',re.S)

def getData(baseurl):  #获取数据
    datalist=[]
    c=0
    for i in range(0,10):  #10次获取，一页25条
        url=baseurl+str(i*25)
        html=askUrl(url)
        soup = BeautifulSoup(html,"lxml") #BeautifulSoup解析
        data = []#用于保存一部的信息
        for item in soup.find_all('div' , class_="item"):
            #print(item)   #测试
            item=str(item)
            link=re.findall(findLink, item)[0]
            img=re.findall(findImg,item)[0]
            title=re.findall(fingTitle,item)
            ranting=re.findall(fingRating,item)[0]
            cnumber=re.findall(findCNumber,item)[0]
            dic = re.findall(findDics, item)
            info = re.findall(findInfo,item)[0]
            info=re.sub('<br(\s+)?/>(/s+)?',"",info)
            info=re.sub('/',"",info)

            data.append(link)
            data.append(img)
            if len(title) == 2:
                ctitle = title[0]
                etitle = title[1]
                data.append(ctitle)
                data.append(etitle)
            else:
                ctitle = title[0]
                etitle = ''
                data.append(ctitle)
                data.append(etitle)
            data.append(ranting)
            data.append(cnumber)
            if len(dic) == 0:
                data.append('')
            else:
                dic=dic[0].replace("。","")
                data.append(dic)
            data.append(info.strip())
            c+=1
            datalist.append(data)
            data=[]
    for items in datalist:
        print(items)
    return datalist



def saveData(datalist,path):  #储存数据
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
    print("test")
    col=('链接','图片链接','中文名','外文名','评分','评价人数','描述','信息')
    for i in range(0,8):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,250):
        print("%d条"%i)
        data=datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save('test1.xls')


def saveData2(datalist,dbpath):
    createdb(dbpath)
    conn = sqlite3.connect(dbpath)
    cur=conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index==5:
                continue
            data[index]='"'+data[index]+'"'
        sql='''
            insert into movie250 (info_link,pic_link,name,ename,cnumber,rate,dec,info)
            values(%s)
            '''%",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    conn.close()

def createdb(dbpath):
    sql='''
    create table movie250
    ( id integer primary key autoincrement,
    info_link text,
    pic_link text,
    name text,
    ename text,
    cnumber numeric,
    rate numeric,
    dec text,
    info text
    )
    '''
    conn = sqlite3.connect(dbpath)
    cur=conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    main()
    print('爬取完毕')