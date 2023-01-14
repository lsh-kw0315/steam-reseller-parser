import urllib.request
import urllib.response
import urllib.error
import urllib.robotparser
from bs4 import BeautifulSoup




url = 'https://directg.net/game/game_thumb.html?page=1'
headers = {'User-Agent': 'Chrome/66.0.3359.181'}
response = None
try:
    # 403 에러를 피하는 용도
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
except urllib.error.URLError as e:
    print(e)
soup=BeautifulSoup(response,'html.parser')
total_str=soup.find('strong',class_='text-primary').text
total_str=total_str.replace(',','')
total=int(total_str)
total_page=total//18;
if total_page==0:
    total_page=1;
if total_page*18<total:
    total_page+=1
response_list=list()
for x in range(total_page):
    tmp_url='https://directg.net/game/game_thumb.html?page=%d'%(x+1)
    request=urllib.request.Request(tmp_url,headers=headers)
    response=urllib.request.urlopen(request)
    response_list.append(response);
game_price_map=dict();
for y in response_list:
    header=y.headers
    p=y.read()
    if(not (header.get_content_charset()=="utf-8" or header.get_content_charset()=="euc-kr")):
        encoding=header.get_content_charset(failobj='utf-8')
        p=p.decode(encoding)
    soup=BeautifulSoup(p,'html.parser')
    pure_price_tag=soup.select('span.PricesalesPrice');
    game_name_tag=soup.select('div.vm-product-descr-container-1>a>h2')
    for i,j in zip(pure_price_tag,game_name_tag):
        pure_price=i.text
        game_name=j.text
        game_name=game_name.replace("\n","")
        game_name=game_name.replace("\t","")
        game_name=game_name.replace(",","")
        game_name=game_name.strip()
        
        pure_price=pure_price.replace("\n","")
        pure_price=pure_price.replace("\t","")
        pure_price=pure_price.replace(",","")
        pure_price=pure_price.strip()
        pure_price=pure_price[1:]
        game_price_map[game_name]=int(pure_price)
        
lower_game=list()
for name,price in game_price_map.items():
    if(price<=10000):
        lower_game.append(name)
for text in lower_game:
    print(text)