import requests
import urllib
n= 2
a=urllib.parse.quote("手机")
print(a)
url = 'https://search.jd.com/Search?' \
                  'keyword='+a+'&enc=utf-8&qrst=1&rt=1&psort=3&stop=1&vt=2&stock=1&page=' + str(n) + '&s=' + str(1 + (n - 1) * 30) + '&click=0&scrolling=y'
head = {'Host': 'search.jd.com',
                    'method': 'GET',
                    'scheme': 'https',
                    'referer': 'https://search.jd.com/Search?keyword='+a+'&enc=utf-8&psort=3',
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'Cookie':'shshshfpa=6d8df1de-1922-9076-db6e-736243584849-1581240019; shshshfpb=tcbssMbcmt4VTUDjenaNlQw%3D%3D; xtest=1562.cf6b6759; qrsc=3; user-key=e841c5a4-8414-4f6f-ac61-41e8235cae0c; cn=0; areaId=19; ipLoc-djd=19-1709-20094-0; PCSYCityID=CN_440000_445200_445203; __jdu=1494461959; unpl=V2_ZzNtbUYARRV9ARNSeh5bA2JXGwpKA0ZAIQxCBC5MXQNkCxUNclRCFnQUR1ZnGFsUZAMZXkJcQRxFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHscVABiBBJVRl9zJXI4dmR9H1wEYwAiXHJWc1chVEBceRBZBCoDF1VHUkQVfQxOZHopXw%3d%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_5f7198d706674e8f9e4de55add07296a|1583500897689; __jdc=122270672; rkv=V0300; 3AB9D23F7A4B3C9B=24Q63VJA6NXWUQBGUQ3TD2PTVB2R5JJSXJ5UZRIX7HLI55HJBNFKXV26DJGHLAZZ5XOJXKIXFP34CO5DXDFAG5M3IU; shshshfp=19368189813c13f760e38886407c5a42; __jda=122270672.1494461959.1577366318.1583500898.1583502931.35; shshshsID=76264d35271119c804db0be2d5d9e372_2_1583503089765; __jdb=122270672.2.1494461959|35.1583502931'
                    }
r = requests.get(url, headers=head)
r.encoding='utf-8'
print(r.text)