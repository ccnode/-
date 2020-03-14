import requests
# 创建代理
def createProxies():
    try:
        # 代理链接（此前使用的是飞蚁代理）
        feiyi = ""
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
