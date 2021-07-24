from flask import Flask,render_template
import sqlite3
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("/index.html")

@app.route('/index')
def index():
    return hello_world()

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

@app.route('/word')
def word():
    return render_template("/word.html")

@app.route('/team')
def team():
    return render_template("/team.html")

if __name__ == '__main__':
    app.run(debug='TRUE')
