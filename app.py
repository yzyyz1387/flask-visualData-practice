from flask import Flask,render_template,request
import sqlite3
import os
import time
app = Flask(__name__)

#主页
@app.route('/')
def hello_world():
    return render_template("/index.html")

#主页
@app.route('/index')
def index():
    return render_template("/index.html")

#信息页面
@app.route('/infor')
def infor():
    datalist=[]
    conn=sqlite3.connect("movie.db")
    cur=conn.cursor()
    sql='''
    select * from movie250
    '''
    data=cur.execute(sql)
    for item in data:
        datalist.append(item)
    conn.commit()
    cur.close()
    conn.commit()
    conn.close()
    return render_template("/infor.html",datalist=datalist)

#评分页面
@app.route('/rate')
def rate():
    datalist = []
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = '''
        select cnumber,count(cnumber) from movie250 group by cnumber
        '''
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    conn.commit()
    cur.close()
    conn.commit()
    conn.close()
    sc=[]
    count=[]
    for data in datalist:
        sc.append(data[0])
        count.append(data[1])
    return render_template("/rate.html",sc=sc,count=count)


#词云页面
@app.route('/word')
def word():
    return render_template("/word.html")

#关于页面
@app.route('/team')
def team():
    return render_template("/team.html")

#留言页面
@app.route("/msg",methods=['POST','GET'])
def msg():
    if request.method == 'POST':
        msg = request.form
        saveMsg(msg,'msg.db')
        smsg=showmsg()
        return render_template("test1.html",smsg=smsg)
    else:
        smsg=showmsg()
        return render_template("test1.html",smsg=smsg)

#留言页面
@app.route('/inmsg')
def inputmsg():
    smsg=showmsg()
    return render_template('test1.html',smsg=smsg)

#创建留言数据库
def createtable(path):
    sql = '''
       create table msgs
       ( id integer primary key autoincrement,
       username text,
       email text,
       msg text,
       msgtime text
       )
       '''
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

#储存留言，传入表单信息和数据库路径
def saveMsg(msglist,dbpath):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 连接数据库
    conn = sqlite3.connect(dbpath)
    cur=conn.cursor()
    #建个空列表存数据
    data=[]
    for ii in msglist.items():
        data.append(ii[1])
    data.append(now)
    for i in range(len(data)):
        data[i]='"'+data[i]+'"'
        #加双引号
    sql='''
            insert into msgs (username,email,msg,msgtime)
            values(%s)
            '''%",".join(data)
    #上面用英文逗号连接要写入的内容
    # print(sql)
    #打印一手，测试用
    cur.execute(sql)
    conn.commit()
    conn.close()

#显示留言
def showmsg():
    if os.path.exists('msg.db') == True:
        #空列表存数据
        datalist = []
        #连接数据库
        conn = sqlite3.connect("msg.db")
        cur = conn.cursor()
        sql = '''
        select * from msgs
        '''
        data = cur.execute(sql)
        #data出来是sqlite的对象，遍历，加入列表datalist
        for item in data:
            datalist.append(item)
        conn.commit()
        cur.close()
        conn.commit()
        conn.close()
        smsgdata=datalist
        #记得用了好几个datalist了，写个smsgdata用一下（ShowMsgData）
        return smsgdata
    else:
        createtable('msg.db')
        datalist = []
        conn = sqlite3.connect("msg.db")
        cur = conn.cursor()
        sql = '''
                select * from msgs
                '''
        data = cur.execute(sql)
        for item in data:
            datalist.append(item)
        conn.commit()
        cur.close()
        conn.commit()
        conn.close()
        smsgdata = datalist
        return smsgdata

if __name__ == '__main__':
    app.run(debug='TRUE')
