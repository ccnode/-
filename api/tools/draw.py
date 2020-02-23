import numpy as np
import matplotlib.pyplot as plt
import os
# 饼状图
async def pie_chart(res,user_id,q_id):

    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    labels = '正面评论', '中等', '负面评论'  # 定义标签

    plt.figure(figsize=(6, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
    plt.title('情感综合分数：{}(满分100)'.format(res["score"]))  # 绘制标题
    sizes = [res["positive"], res["medium"], res["negative"]]  # 每一块的比例
    colors = ['yellowgreen', 'gold', 'lightcoral']  # 每一块的颜色
    explode = (0.01, 0.01, 0.01)  # 突出显示，这里仅仅突出红色

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=70)

    plt.axis('equal')  # 显示为圆（避免比例压缩为椭圆）
    # 图片存储路径
    path = '../../source/user/{}/{}'.format(user_id, q_id)
    if (os.path.exists(path) == False):
        os.makedirs(path)
    plt.savefig(path + '/sentiment.png')
    # plt.show()
if __name__ == '__main__':
    pie_chart()