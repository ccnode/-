import requests
from lxml import etree
from api.tools.back_dbtools import DB2
import urllib
import asyncio
from fake_useragent import UserAgent
import api.tools.proxies as proxies
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
    #
    async def start(self):
        ua = UserAgent()
        # 创建代理
        p = proxies.createProxies()
        n = int(self.n)
        data = ""
        q_keyword = urllib.parse.quote(self.keyword)
        for i in range(1,n+1):
            #构造每一页的url变化
            url = 'https://search.jd.com/Search?' \
                  'keyword='+q_keyword+'&enc=utf-8&qrst=1&rt=1&psort=3&stop=1&vt=2&stock=1&' \
                   'page=' + str(i) + '&s=' + str(1 + (i - 1) * 30) + \
                  '&click=0&scrolling=y'
            print(url)
            head = {'Host': 'search.jd.com',
                    'method': 'GET',
                    'scheme': 'https',
                    'user-agent': ua.chrome,
                    'x-requested-with': 'XMLHttpRequest',
                    'Cookie':'shshshfpa=6d8df1de-1922-9076-db6e-736243584849-1581240019; shshshfpb=tcbssMbcmt4VTUDjenaNlQw%3D%3D; xtest=1562.cf6b6759; qrsc=3; user-key=e841c5a4-8414-4f6f-ac61-41e8235cae0c; cn=0; areaId=19; ipLoc-djd=19-1709-20094-0; PCSYCityID=CN_440000_445200_445203; __jdu=1494461959; unpl=V2_ZzNtbUYARRV9ARNSeh5bA2JXGwpKA0ZAIQxCBC5MXQNkCxUNclRCFnQUR1ZnGFsUZAMZXkJcQRxFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHscVABiBBJVRl9zJXI4dmR9H1wEYwAiXHJWc1chVEBceRBZBCoDF1VHUkQVfQxOZHopXw%3d%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_5f7198d706674e8f9e4de55add07296a|1583500897689; __jdc=122270672; rkv=V0300; 3AB9D23F7A4B3C9B=24Q63VJA6NXWUQBGUQ3TD2PTVB2R5JJSXJ5UZRIX7HLI55HJBNFKXV26DJGHLAZZ5XOJXKIXFP34CO5DXDFAG5M3IU; shshshfp=19368189813c13f760e38886407c5a42; __jda=122270672.1494461959.1577366318.1583500898.1583502931.35; shshshsID=76264d35271119c804db0be2d5d9e372_2_1583503089765; __jdb=122270672.2.1494461959|35.1583502931'
                    }
            if p:
                r = requests.get(url, headers=head,proxies=p)
            else:
                r = requests.get(url, headers=head)
            #获取各项数据组成SQL语句
            data += await self.parser(r,self.q_id)
            await asyncio.sleep(1)
        sql = "insert into k_goods_info(q_id,goods_name,shop_name,goods_price) values" + data
        sql = sql[:-1]
        sql += ";"
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
        item["shop_name"] = []
        item["goods_price"] = []
        for key in keys:
            # 商品名
            nameList = key.xpath("div[@class='p-name p-name-type-2']/a/em/text()")
            if nameList :
                goods_name = ",".join(nameList)
                goods_name = goods_name.replace("'","")
                item["goods_name"].append(goods_name)
                # 店铺名
                shop_name = key.xpath("div[@class='p-shop']/span/a/@title")
                # 据观察，爬取不到的店铺都是京东自营
                if shop_name:
                    item["shop_name"].append(shop_name[0])
                else:
                    shop_name = "京东自营"
                    item["shop_name"].append(shop_name[0])
                # 价格，存在两种爬取方式，若爬不到则设为0
                goods_price = key.xpath("div[@class='p-price']/strong/i/text()")
                if goods_price:
                    item["goods_price"].append(goods_price[0])
                else:
                    goods_price = key.xpath("div[@class='p-price']/strong/@data-price")
                    if goods_price:
                        item["goods_price"].append(goods_price[0])
                    else:
                        goods_price = 0
                        item["goods_price"].append(goods_price)
            # 测试
            # print(key.xpath("div[@class='p-name p-name-type-2']/a/em/text()"),key.xpath("div[@class='p-shop']/span/a/@title"),key.xpath("div[@class='p-price']/strong/i/text()"),key.xpath("div[@class='p-price']/strong/@data-price"))
            # print(goods_name,shop_name,goods_price)
        # print(len(item["goods_name"]), len(item["shop_name"]), len(item["goods_price"]))
        # return
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
    spider = crow_keyword( 3, "鞋子", 11)
    spider.coroutines()

