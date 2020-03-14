import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import sys
from wordcloud import WordCloud,STOPWORDS
import jieba
from PIL import Image
import asyncio

# 散点图
async def scatter(data):
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    plt.figure(figsize=(11, 7))

    x = data["x"]
    y = data["y"]
    plt.scatter(x, y)
    plt.xlabel("商品号")
    plt.ylabel("价格(元)")
    plt.title(data["title"],color='r',fontdict={'weight':'normal','size': 15})
    plt.grid(True)  # 显示网格线
    # 保存生成的图片
    path = sys.argv[0]+'/../static/source/user/{}/keyword/{}'.format(data["user_id"], data["q_id"])
    if (os.path.exists(path) == False):
        os.makedirs(path)
    plt.savefig(path + '/price_distribution.png')
    # plt.show()
    print("评论统计图绘制完毕！")

# 柱状图
async def histogram(data):
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    fig, ax = plt.subplots(figsize=(15, 11))

    x = data["x"]
    y = data["y"]
    ax.barh(x, y, color="blue")

    ax.set(xlabel="商品数", title="top10商品排名")


    # 保存生成的图片
    path = sys.argv[0]+'/../static/source/user/{}/keyword/{}'.format(data["user_id"], data["q_id"])
    if (os.path.exists(path) == False):
        os.makedirs(path)
    plt.savefig(path + '/shop_ranking.png')
    # plt.show()
    print("店铺排名图绘制完毕！")
