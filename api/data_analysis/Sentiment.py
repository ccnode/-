from snownlp import SnowNLP
from api.tools.dbtools import DB
import asyncio
from api.tools import draw
# 情感分析
async def Sentiment(loop):
    list = []
    count = 0
    db = DB(dbname="mitucat",loop=loop)
    q_data = await db.query("select content from comments_info where goods_id=1")
    # 计算每条评论的情感倾向指数
    for i in q_data:
        s = SnowNLP(i[0])
        list.append(round(s.sentiments,3))
    res = await get_calculate(list)
    print("z：{}".format(res))
    print("开始绘制")
    await draw.pie_chart(res,1,1)

# 计算情感平均分数，正向中等负向占比
async def get_calculate(list):
    sum = 0
    positive = 0
    medium = 0
    num = len(list)
    results = dict()
    # 平均数
    for n in list:
        sum += n
        if n >= 0.7:
            positive +=1
        elif n<=0.3:
            medium +=1

    print(positive,medium)
    results["score"] = round(sum/num,3)*100
    results["positive"] = round(positive/num,3)
    results["medium"] = round(medium/num,3)
    results["negative"] = round(1-results["positive"]-results["medium"],3)
    print(results["positive"]+results["medium"]+results["negative"])
    return results



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Sentiment(loop))

