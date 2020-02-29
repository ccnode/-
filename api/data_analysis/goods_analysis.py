from snownlp import SnowNLP
from api.tools.back_dbtools import DB
import asyncio
from api.data_analysis import g_draw as draw
import datetime
class goods_analysis():
    def __init__(self,q_id):
        self.q_id = q_id
        loop = asyncio.get_event_loop()
        self.loop = loop
        self.db = DB(dbname="mitucat", loop=self.loop)
        self.loop.run_until_complete(self.start())
        self.loop.close()

    # 启动主体
    async def start(self):
        self.q_data = await self.db.query(
            "select q.id,q.user_id,c.content,c.com_date "
            "from goods_query_log q left join goods_info i on q.id=i.q_id "
            "left join comments_info c on i.id=c.goods_id "
            "where q.id=" + str(self.q_id) + " order by c.com_date asc ")

        # 赋值user_id
        self.user_id = self.q_data[0][1]

        # 生成评论统计
        await self.c_statistical()

        #生成情感分析图
        await self.Sentiment()

        #生成词云
        await self.word_frequency()

    # 评论统计
    async def c_statistical(self):
        count = 0
        t = 0
        count_list = []
        data = self.q_data
        date_list = await self.getDatesByTimes(data[0][3],data[-1][3])
        # 计算每天有多少数量
        for date in date_list:
            for j in range(t,len(data)):
                if date == data[j][3].strftime('%Y-%m-%d'):
                    count += 1
                else:
                    count_list.append(count)
                    count = 0
                    t = j
                    break
        # 添加最后一个统计
        count_list.append(count)

        res = {"x": date_list, "y": count_list, "title": "每日评论数统计",
               "user_id":self.user_id,"q_id":self.q_id}
        await draw.line_chart(res)

    # 根据开始日期、结束日期返回这段时间里所有天的集合
    async def getDatesByTimes(self,sDateStr, eDateStr):
        list = []
        # datestart = sDateStr.date()
        # dateend = eDateStr.date()
        datestart = sDateStr
        dateend = eDateStr
        list.append(datestart.strftime('%Y-%m-%d'))
        while datestart < dateend:
            datestart += datetime.timedelta(days=1)
            list.append(datestart.strftime('%Y-%m-%d'))
        return list


    # 情感分析
    async def Sentiment(self):
        list = []
        # 计算每条评论的情感倾向指数
        for i in self.q_data:
            s = SnowNLP(i[2])
            list.append(round(s.sentiments,3))
        res = await self.get_calculate(list)
        res["user_id"]=self.user_id
        res["q_id"]=self.q_id
        print("绘制情感分析图..")
        await draw.pie_chart(res)

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
            text +=i[2]+";"
        res={"text":text,"user_id":self.user_id,"q_id":self.q_id}
        await draw.word_cloud(res)

if __name__ == '__main__':
    analysis = goods_analysis(11)

