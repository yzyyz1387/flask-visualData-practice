# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 11:25
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : testwordcloud.py
# @Software: PyCharm

from wordcloud import WordCloud  #词云
import jieba  #分词
from matplotlib import pyplot as plt  #绘图 数据可视化
from PIL import Image #图像处理
import numpy as np
import sqlite3


#连接数据库获取数据
conn = sqlite3.connect('movie.db')
cur= conn.cursor()
sql ='''
select dec from movie250
'''
data=cur.execute(sql)
text=""
for item in data:
    text = text+item[0]
cur.close()
conn.close()

# 分词
cut = jieba.cut(text)
string=" ".join(cut)
print(len(string))

#绘图遮罩配置等
img=Image.open(r'.\static\asstes\test.jpg')
imgarray=np.array(img)
wc=WordCloud(
    background_color='#ffffff',
    mask=imgarray,
    font_path="msyh.ttc",
)
wc.generate_from_text(string)

#绘制
fig=plt.figure(1)
plt.imshow(wc)
plt.axis('off')   #是否显示坐标轴
# plt.show()
wc.to_file('static/asstes/word.jpg')  #保存图片
