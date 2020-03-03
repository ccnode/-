import requests
from lxml import etree
from api.tools.back_dbtools import DB2
import asyncio
class crow_keyword():
    def __init__(self,n,keyword,q_id):
        self.n = n
        self.keyword = keyword
        self.q_id = q_id
    def coroutines(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.start())
        self.loop.close()
    #定义函数抓取每页前30条商品信息
    async def start(self):
        n = int(self.n)
        count = 0
        sql = ""
        for i in range(1,n+1):
            count+=1
            #构造每一页的url变化
            url = 'https://search.jd.com/Search?' \
                  'keyword='+str(self.keyword)+'&enc=utf-8&qrst=1&rt=1&psort=3&stop=1&vt=2&stock=1&page=' + str(n) + '&s=' + str(1 + (n - 1) * 30) + '&click=0&scrolling=y'
            head = {'authority': 'search.jd.com',
                    'method': 'GET',
                    'path': '/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=4&s=84&scrolling=y&log_id=1529828108.22071&tpl=3_M&show_items=7651927,7367120,7056868,7419252,6001239,5934182,4554969,3893501,7421462,6577495,26480543553,7345757,4483120,6176077,6932795,7336429,5963066,5283387,25722468892,7425622,4768461',
                    'scheme': 'https',
                    'referer': 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=58&click=0',
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'Cookie':'qrsc=3; pinId=RAGa4xMoVrs; xtest=1210.cf6b6759; ipLocation=%u5E7F%u4E1C; _jrda=5; TrackID=1aUdbc9HHS2MdEzabuYEyED1iDJaLWwBAfGBfyIHJZCLWKfWaB_KHKIMX9Vj9_2wUakxuSLAO9AFtB2U0SsAD-mXIh5rIfuDiSHSNhZcsJvg; shshshfpa=17943c91-d534-104f-a035-6e1719740bb6-1525571955; shshshfpb=2f200f7c5265e4af999b95b20d90e6618559f7251020a80ea1aee61500; cn=0; 3AB9D23F7A4B3C9B=QFOFIDQSIC7TZDQ7U4RPNYNFQN7S26SFCQQGTC3YU5UZQJZUBNPEXMX7O3R7SIRBTTJ72AXC4S3IJ46ESBLTNHD37U; ipLoc-djd=19-1607-3638-3638.608841570; __jdu=930036140; user-key=31a7628c-a9b2-44b0-8147-f10a9e597d6f; areaId=19; __jdv=122270672|direct|-|none|-|1529893590075; PCSYCityID=25; mt_xid=V2_52007VwsQU1xaVVoaSClUA2YLEAdbWk5YSk9MQAA0BBZOVQ0ADwNLGlUAZwQXVQpaAlkvShhcDHsCFU5eXENaGkIZWg5nAyJQbVhiWR9BGlUNZwoWYl1dVF0%3D; __jdc=122270672; shshshfp=72ec41b59960ea9a26956307465948f6; rkv=V0700; __jda=122270672.930036140.-.1529979524.1529984840.85; __jdb=122270672.1.930036140|85.1529984840; shshshsID=f797fbad20f4e576e9c30d1c381ecbb1_1_1529984840145'
                    }
            r = requests.get(url, headers=head)
            sql += await self.parser(r,self.q_id)

            if i == n:
                sql = "insert into k_goods_info(q_id,goods_name,shop_name,goods_price) values" + sql
                sql = sql[:-1]
                sql += ";"

            print("等待")
            await asyncio.sleep(1)

        await self.inputmysql(sql)

    # 解析页面
    async def parser(self,r,q_id):
        # 指定编码方式，不然会出现乱码
        r.encoding = 'utf-8'
        html = etree.HTML(r.text)
        # 定位到每一个商品标签
        keys = html.xpath("//div[@class='gl-i-wrap']")
        # 创建字典
        item = dict()
        item["goods_name"] = []
        for key in keys:
            nameList = key.xpath("div[@class='p-name p-name-type-2']/a/em/text()")
            name = ",".join(nameList)
            item["goods_name"].append(name)
        item["shop_name"] = html.xpath("//div[@class='p-shop']/span/a/@title")
        item["goods_price"] = html.xpath("//div[@class='p-price']/strong/i/text()")
        # item["comments_num"] = html.xpath("//div[@class='p-commit']/strong/a/text()")

        data = ""
        # 解析并编写sql
        for i in range(len(item["goods_name"])):
            goods_name = item["goods_name"][i]
            shop_name = item["shop_name"][i]
            goods_price = item["goods_price"][i]
            # comments_num = item["comments_num"][i]
            data += "({},'{}','{}',{}),".format(q_id, goods_name, shop_name, goods_price)
        return data
    # 操作数据库
    async def inputmysql(self,sql):
        db = DB2(self.loop)
        await db.commit(sql)


if __name__=='__main__':
    spider = crow_keyword( 3, "衣服", 11)
    spider.coroutines()

