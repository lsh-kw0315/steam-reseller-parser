from bs4 import BeautifulSoup
from urllib.request import Request
from urllib.request import urlopen
import urllib.error
from json import loads
from sys import argv
from math import trunc
from time import sleep
from pandas import DataFrame
url='https://www.humblebundle.com/store/api/search?sort=bestselling&filter=all&hmb_source=navbar{0}&request=1'
json_url=url.format("")
headers = {'User-Agent': 'Chrome/66.0.3359.181'}
standard_price=5
standard_discount=30
if len(argv)>1:
    if argv[1].isdigit():
        standard_price=int(argv[1])

if len(argv)>2:
    if argv[2].isdigit():
        standard_discount=int(argv[2])
cnt=0
game_price_map=dict()
game_discount_map=dict()
while True:
    if cnt>0:
        json_url=url.format("&page={0}".format(cnt))
    response=None
    try:
        request=Request(json_url,headers=headers)
        response=urlopen(request)
    except urllib.error.URLError as e:
        selection=input("your connection is blocked. wait 15 minutes?(if you want to wait, input 0.)")
        if(selection.isdigit() and int(selection)==0):
            sleep(60*17)
        else:
            break
    except Exception:
        break
    header=response.headers
    p=response.read()
    if header.get_content_charset() != "utf-8":
        encoding=header.get_content_charset(failobj='utf-8')
        p=p.decode(encoding)
    html=BeautifulSoup(p,'html.parser')
    to_json=loads(html.prettify())
    result_list=to_json['results']
    for result in result_list:
        if(result['cta_badge']=='coming_soon'):
            continue
        if(result['current_price']['amount']<=standard_price):
            game_price_map[result['human_name']]=result['current_price']['amount']
            
        discount=(1-result['current_price']['amount']/result['full_price']['amount'])*100
        discount=trunc(discount)
        if(discount>=standard_discount):
            game_discount_map[result['human_name']]=discount
    cnt+=1
    sleep(1);
f1=open('HBbundle_price_list.txt','w',encoding='utf-8')
f2=open('HBbundle_discount_list.txt','w',encoding='utf-8')
df_price=DataFrame.from_dict([game_price_map])
df_discount=DataFrame.from_dict([game_discount_map])
df_price=df_price.melt(var_name='game',value_name='price')
df_discount=df_discount.melt(var_name="game",value_name="discount") 
df_price.to_excel('HBbundle_price_list.xlsx')
df_discount.to_excel('HBbundle_discount_list.xlsx')
for game in game_price_map.keys():
    f1.write(game+'\n')
for game in game_discount_map.keys():
    f2.write(game+'\n')
f2.close()
print("task finished.")