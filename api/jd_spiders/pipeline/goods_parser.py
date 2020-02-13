from lxml import etree
import time
import asyncio

# from spiders.jd_spider import goods_item
# 解析商品页面
async def parser(browser,page,url,db):
    await asyncio.sleep(1)
    print("下载页面。。。")
    t1 = time.time()
    text = await page.content()
    # 关闭页面
    await browser.close()

    html = etree.HTML(text)
    t2 = time.time()
    print("下载耗时：{}".format(t2-t1))
    # 获取数据
    goods_name = html.xpath("//title/text()")
    goods_price = html.xpath("//span[@class='p-price']/span[2]/text()")
    comments_num = html.xpath("//div[@id='comment-count']/a/text()")
    shop_name = html.xpath("//div[@class='mt']/h3/a/text()")

    # 数据整合
    data = "{},'{}','{}',{},'{}','{}',{}".format(1,goods_name[0],shop_name[0],goods_price[0],comments_num[0],url,0)
    print(data)
    # 创建数据库实例
    # sql = "insert into goods_info(q_id,goods_name,shop_name,goods_price,comments_num,link_url,q_type) values("+data+")"
    sql = "insert into goods_info(q_id,goods_name,shop_name,goods_price,comments_num,link_url,q_type) values("+data+")"

    # sql = "select * from user_info"
    print(sql)
    res = await db.commit(sql)
    print(res)
    
    # 关闭浏览器
    # await page.close()
    


# 合并列表
async def mergeList(lists):
    str = ""
    for i in lists:
        # str +=i.replace(" ","").replace("\n","").replace("\r","")
        str +=i.strip()
    return str