import requests
# 创建代理
def createProxies():
    try:
        # 代理链接（此前使用的是飞蚁代理）
        feiyi = "http://183.129.244.16:88/open?user_name=ccnodeap1&timestamp=1584186231&md5=E54A4E9352B92B073531259E0ECDBEDF&pattern=json&number=1"
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
