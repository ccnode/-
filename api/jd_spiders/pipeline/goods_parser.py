from lxml import etree
from api.tools import md5
import time
import asyncio
from api.jd_spiders.pipeline import comments_parser as c
# 解析商品页面
async def parser(page,url,num):
    await page.waitFor(1000)
    print("获取商品信息中。。。")
    text = await page.content()
    html = etree.HTML(text)

    # 获取数据
    goods_name = html.xpath("//title/text()")
    goods_price = html.xpath("//span[@class='p-price']/span[2]/text()")
    comments_num = html.xpath("//li[@data-anchor='#comment']/s/text()")
    shop_name = html.xpath("//div[@class='mt']/h3/a/text()")
    if shop_name == []:
        shop_name = html.xpath("//div[@class='name']/a/text()")

    # 测试
    # print("data:{},'{}','{}',{},".format(goods_name,shop_name,goods_price,comments_num))
    # 数据整合，编写sql
    data = "{},'{}','{}',{},'{}','{}',{}".format(1,goods_name[0],shop_name[0],goods_price[0],(comments_num[0]).strip('()'),url,0)
    print(data)
    sql = "insert into goods_info(q_id,goods_name,shop_name,goods_price,comments_num,link_url,q_type) values("+data+");SELECT LAST_INSERT_ID();"
    print("获取成功！")

    # 返回sql给主程序
    return sql


# 合并列表
async def mergeList(lists):
    str = ""
    for i in lists:
        # str +=i.replace(" ","").replace("\n","").replace("\r","")
        str +=i.strip()
    return str