from lxml import etree
import asyncio

# 解析商品页面
async def parser(page,num,q_id):
    data = ""
    count = 0
    while True:
        # 点击评价数跳转
        await asyncio.sleep(1.3)
        await page.hover("a[class='pn-next']")
        await asyncio.sleep(1.3)
        #开始爬取本页数据
        # 获取商品信息的标签并下载所有元素
        el = await page.querySelector("ul[class='gl-warp clearfix']")
        text = await page.evaluate('(element) => element.innerHTML',el)
        html = etree.HTML(text)

        # 获取这一页商品标签列表
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
        item["comments_num"] = html.xpath("//div[@class='p-commit']/strong/a/text()")
        # 解析并编写sql
        for i in range(len(item["goods_name"])):
            goods_name = item["goods_name"][i]
            shop_name = item["shop_name"][i]
            goods_price = item["goods_price"][i]
            comments_num = item["comments_num"][i]
            if count == num - 1:
                data += "({},'{}','{}',{},'{}',{});".format(q_id,goods_name,shop_name,goods_price,comments_num,1)
                count += 1
                break
            else:
                data += "({},'{}','{}',{},'{}',{}),".format(q_id,goods_name,shop_name,goods_price,comments_num,1)
            # 计数器+1
            count += 1
        print("已爬取：{}个商品".format(count))
        if count == num:
            break
        # 翻页
        await page.hover("a[class='pn-next']")
        await page.waitFor(300)
        await asyncio.sleep(0.3)
        await page.click("a[class='pn-next']")
    sql = "insert into goods_info(q_id,goods_name,shop_name,goods_price,comments_num,q_type) values" + data
    return sql