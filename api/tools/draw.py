import numpy as np
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, ImageColorGenerator,STOPWORDS
import jieba
from PIL import Image
import re
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

# 词云
async def word_cloud(text,user_id,q_id):
    # 图片模板和字体
    image = np.array(Image.open(r'img/background.jpg'))
    font = r'font/simfang.ttf'

    # 分词
    wordlist_after_jieba = jieba.cut(text)
    wl_space_split = " ".join(wordlist_after_jieba)

    # 设置停用词
    sw = set(STOPWORDS)
    sw.add("京东")

    # 关键一步
    my_wordcloud = WordCloud(scale=2, font_path=font, mask=image, stopwords=sw, background_color='white',
                             max_words=200, max_font_size=60, random_state=20).generate(wl_space_split)

    # 显示生成的词云
    plt.imshow(my_wordcloud)
    plt.axis("off")
    # 保存生成的图片
    path = '../../source/user/{}/{}'.format(user_id, q_id)
    if (os.path.exists(path) == False):
        os.makedirs(path)
    my_wordcloud.to_file(path + '/wordcloud.png')
    plt.show()




if __name__ == '__main__':
    pie_chart()