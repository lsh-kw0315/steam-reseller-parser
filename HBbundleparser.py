from bs4 import BeautifulSoup
import urllib.request
import urllib.response
import urllib.error
import json
import sys
import math
url='https://www.humblebundle.com/store/api/search?sort=bestselling&filter=all&hmb_source=navbar{0}&request=1'
json_url=url.format("")
headers = {'User-Agent': 'Chrome/66.0.3359.181'}
standard_price=5
standard_discount=30
if len(sys.argv)>1:
    if sys.argv[1].isdigit():
        standard_price=int(sys.argv[1])

if len(sys.argv)>2:
    if sys.argv[2].isdigit():
        standard_discount=int(sys.argv[2])
cnt=0
game_price_map=dict()
game_discount_map=dict()
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
        if(result['current_price']['amount']<=standard_price):
            game_price_map[result['human_name']]=result['current_price']['amount']
            
        discount=(1-result['current_price']['amount']/result['full_price']['amount'])*100
        discount=math.trunc(discount)
        if(discount>=standard_discount):
            game_discount_map[result['human_name']]=discount
    cnt+=1
f1=open('HBbundle_price_list.txt','w',encoding='utf-8')
f2=open('HBbundle_discount_list.txt','w',encoding='utf-8')
for game in game_price_map.keys():
    f1.write(game+'\n')
for game in game_discount_map.keys():
    f2.write(game+'\n')
f2.close()
print("task finished.")