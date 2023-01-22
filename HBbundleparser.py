from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import urllib.error
import json
import sys

url='https://www.humblebundle.com/store/api/search?sort=bestselling&filter=all&hmb_source=navbar{0}&request=1'
json_url=url.format("")
headers = {'User-Agent': 'Chrome/66.0.3359.181'}
standard=5
if len(sys.argv)>1:
    if sys.argv[1].isdigit():
        standard=int(sys.argv[1])
    
cnt=0
game_price_map=dict()
while True:
    if cnt>0:
        json_url=url.format("&page={0}".format(cnt))
    response=None
    try:
        request=urllib.request.Request(json_url,headers=headers)
        response=urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        print(e)
        break
    except Exception:
        break
    header=response.headers
    p=response.read()
    if header.get_content_charset() != "utf-8":
        encoding=header.get_content_charset(failobj='utf-8')
        p=p.decode(encoding)
    html=BeautifulSoup(p,'html.parser')
    to_json=json.loads(html.prettify())
    result_list=to_json['results']
    for result in result_list:
        if(result['cta_badge']=='coming_soon'):
            continue
        if(result['current_price']['amount']<standard):
            game_price_map[result['human_name']]=result['current_price']['amount']
    cnt+=1
f=open('HBbundlelist.txt','w',encoding='utf-8')
for game in game_price_map.keys():
    f.write(game+'\n')
f.close()
print("task finished.")