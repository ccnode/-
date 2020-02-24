from snownlp import SnowNLP
from api.tools.dbtools import DB
import asyncio
from api.tools import draw
class goods_analysis():
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.loop = loop
        self.db = DB(dbname="mitucat", loop=self.loop)
        self.loop.run_until_complete(self.start())
        self.loop.close()

    # 启动主体
    async def start(self):
        self.q_data = await self.db.query("select * from comments_info where goods_id=1")
        #生成情感分析图
        #await self.Sentiment()

        #生成词云
        await self.word_frequency()

    # 情感分析
    async def Sentiment(self):
        list = []
        # 计算每条评论的情感倾向指数
        for i in self.q_data:
            s = SnowNLP(i[3])
            list.append(round(s.sentiments,3))
        res = await self.get_calculate(list)
        print("绘制情感分析图..")
        await draw.pie_chart(res,1,1)

    # 计算情感平均分数，正向中等负向占比
    async def get_calculate(self,list):
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


        results["score"] = round(sum/num,3)*100
        results["positive"] = round(positive/num,3)
        results["medium"] = round(medium/num,3)
        results["negative"] = round(1-results["positive"]-results["medium"],3)
        print(results["positive"]+results["medium"]+results["negative"])
        return results

    # 词频分析
    async def word_frequency(self):
        text = ""
        # 计算每条评论的情感倾向指数
        for i in self.q_data:
            text +=i[3]+";"

        await draw.word_cloud(text,1,1)

if __name__ == '__main__':
    analysis = goods_analysis()

