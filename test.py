from snownlp import SnowNLP
from api.tools.back_dbtools import DB
import asyncio


async def Sentiment(loop):
    res = []
    count = 0
    db = DB(dbname="mitucat",loop=loop)
    q_data = await db.query("select content from comments_info where goods_id=1")
    # 计算每条评论的情感倾向指数
    for i in q_data:
        s = SnowNLP(i[0])
        res.append(round(s.sentiments,3))

    print("z：{}".format(await get_calculate(res)))

# 计算情感平均分数，正向负向占比
async def get_calculate(list):
    print(list)
    sum = 0
    count = 0
    num = len(list)
    results = dict()
    # 平均数
    for n in list:
        sum += n
        if n >= 0.5:
            count +=1
    results["score"] = round(sum/num,3)*100
    results["positive"] = round(count/num,3)
    results["negative"] = round(1 - results["positive"],3)

    return results

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Sentiment(loop))






