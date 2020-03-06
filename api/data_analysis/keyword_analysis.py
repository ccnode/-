from api.tools.back_dbtools import DB2
import asyncio
from api.data_analysis import k_draw as draw
from collections import Counter
class keyword_analysis():
    def __init__(self,q_id):
        self.q_id = q_id
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        self.loop = loop
        self.db = DB2(dbname="mitucat", loop=self.loop)
        self.loop.run_until_complete(self.start())
        self.loop.close()

    # 启动主体
    async def start(self):
        self.q_data = await self.db.query(
            "select q.id,q.user_id,i.shop_name,i.goods_price,i.comments_num "
            "from keyword_query_log q left join k_goods_info i on q.id=i.q_id "
            "where q.id="+str(self.q_id))
        # 赋值user_id
        self.user_id = self.q_data[0][1]


        # 生成价格区间
        await self.price_distribution()

        #生成店铺排名
        await self.shop_ranking()
    # 价格区间
    async def price_distribution(self):
        # 价格列表
        price_list = []
        for i in self.q_data:
            price_list.append(i[3])

        num_list = []
        num = len(price_list)
        for n in range(1,num+1):
            num_list.append(n)

        res = {"x": num_list, "y": price_list, "title": "top"+str(num)+"商品价格分布",
                "user_id": self.user_id, "q_id": self.q_id}
        await draw.scatter(res)

    # 店铺排名
    async def shop_ranking(self):
        # 取出店铺列表
        shop_list = []
        for i in self.q_data:
            shop_list.append(i[2])
        topshop_list = []
        count_list = []
        list = Counter(shop_list).most_common(10)
        for i in range(len(list)-1,-1,-1):
            topshop_list.append(list[i][0])
            count_list.append(list[i][1])
        res = {"x":topshop_list,"y":count_list,"user_id":self.user_id,"q_id":self.q_id}
        await draw.histogram(res)

if __name__ == '__main__':
    analysis = goods_analysis(2)