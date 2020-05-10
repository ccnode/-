import requests
from lxml import etree
from api.tools.back_dbtools import DB2
from api.jd_spiders import crow_comments
import asyncio
import re
import json
from fake_useragent import UserAgent
import api.tools.proxies as proxies
class crow_goods():
    def __init__(self,url,n,q_id):
        self.n = n
        self.url = url
        self.q_id = q_id
    def coroutines(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        self.loop = asyncio.get_event_loop()
        goods_name = self.loop.run_until_complete(self.start())
        self.loop.close()
        return goods_name
    #爬取商品信息
    async def start(self):
        #创建请求头
        ua = UserAgent()
        head = {'authority': 'search.jd.com',
                            'method': 'GET',
                            'path': '/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=4&s=84&scrolling=y&log_id=1529828108.22071&tpl=3_M&show_items=7651927,7367120,7056868,7419252,6001239,5934182,4554969,3893501,7421462,6577495,26480543553,7345757,4483120,6176077,6932795,7336429,5963066,5283387,25722468892,7425622,4768461',
                            'scheme': 'https',
                            'referer': 'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=58&click=0',
                            'user-agent': ua.chrome,
                            'x-requested-with': 'XMLHttpRequest',
                            'Cookie':'qrsc=3; pinId=RAGa4xMoVrs; xtest=1210.cf6b6759; ipLocation=%u5E7F%u4E1C; _jrda=5; TrackID=1aUdbc9HHS2MdEzabuYEyED1iDJaLWwBAfGBfyIHJZCLWKfWaB_KHKIMX9Vj9_2wUakxuSLAO9AFtB2U0SsAD-mXIh5rIfuDiSHSNhZcsJvg; shshshfpa=17943c91-d534-104f-a035-6e1719740bb6-1525571955; shshshfpb=2f200f7c5265e4af999b95b20d90e6618559f7251020a80ea1aee61500; cn=0; 3AB9D23F7A4B3C9B=QFOFIDQSIC7TZDQ7U4RPNYNFQN7S26SFCQQGTC3YU5UZQJZUBNPEXMX7O3R7SIRBTTJ72AXC4S3IJ46ESBLTNHD37U; ipLoc-djd=19-1607-3638-3638.608841570; __jdu=930036140; user-key=31a7628c-a9b2-44b0-8147-f10a9e597d6f; areaId=19; __jdv=122270672|direct|-|none|-|1529893590075; PCSYCityID=25; mt_xid=V2_52007VwsQU1xaVVoaSClUA2YLEAdbWk5YSk9MQAA0BBZOVQ0ADwNLGlUAZwQXVQpaAlkvShhcDHsCFU5eXENaGkIZWg5nAyJQbVhiWR9BGlUNZwoWYl1dVF0%3D; __jdc=122270672; shshshfp=72ec41b59960ea9a26956307465948f6; rkv=V0700; __jda=122270672.930036140.-.1529979524.1529984840.85; __jdb=122270672.1.930036140|85.1529984840; shshshsID=f797fbad20f4e576e9c30d1c381ecbb1_1_1529984840145'
                            }
        # 获取商品名，店铺名接口
        url = self.url
        # 创建代理
        p = proxies.createProxies()
        if p:
            r = requests.get(url, headers=head, proxies=p)
        else:
            r = requests.get(url, headers=head)
        #提取数据
        html1 = etree.HTML(r.text)
        goods_name = html1.xpath("//title/text()")[0]
        # shop_name = html1.xpath("//div[@class='mt']/h3/a/text()")
        # print(shop_name)
        # if shop_name == []:
        #     shop_name = html1.xpath("//div[@class='name']/a/text()")
        # if shop_name == []:
        #     shop_name=""
        # print(shop_name)
        # 获取价格接口
        # 首先取出商品id拼接url
        href = html1.xpath("//link[@rel='canonical']/@href")
        product_id = re.findall('\d+',href[0])
        url = "https://p.3.cn/prices/mgets?skuIds=J_"+product_id[0]
        r = requests.get(url, headers=head)
        list = json.loads(r.text)
        goods_price = list[0]["p"]
        # 整合商品数据
        data = "({},'{}',{});".format(self.q_id,goods_name,goods_price)
        sql = "insert into goods_info(q_id,goods_name,goods_price) values" + data
        print(sql)
        # 插入数据库获取goods_id
        db = DB2(self.loop)
        goods_id = await db.commits(sql)
        # 爬取评论信息
        comsql = await crow_comments.Commentsparser(goods_id[0][0], product_id[0], self.n,p)
        # 评论数据插入
        await db.commit(comsql)
        # 返回商品名称
        return goods_name
if __name__=='__main__':
    spider = crow_goods(url="https://item.jd.com/42808267238.html", n=2,q_id=11)
    spider.coroutines()
