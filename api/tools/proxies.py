import requests
# 创建代理
def createProxies():
    try:
        # 代理链接（此前使用的是飞蚁代理）
        feiyi = "http://183.129.244.16:88/open?user_name=ccnodeap1&timestamp=1584178688&md5=CF8D0EEC74F1F4E092F683C995F039D7&pattern=json&number=1"
        ipJson = requests.get(feiyi)
        ipJson = ipJson.json()
        proxy =ipJson["domain"]+":"+str(ipJson["port"][0])
        proxies={
            'http':'http://'+proxy,
            'https':'https://'+proxy
        }
        print(ipJson,proxy)
        return proxies
    except:
        return ""
