import urllib.request
import urllib.response
import urllib.error
from bs4 import BeautifulSoup
import sys
url='https://store.steampowered.com/search/?ignore_preferences=1&ndl=1&page=0'
standard=5000
cnt=0
if len(sys.argv)>1:
    if sys.argv[1].isdigit():
        standard=int(sys.argv[1])
game_price_map=dict()
while(True):
    headers = {'User-Agent': 'Chrome/66.0.3359.181'}
    url=url.replace('page={0}'.format(cnt),'page={0}'.format(cnt+1))
    response=None
    try:
        request=urllib.request.Request(url,headers=headers)
        response=urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        print(e)
    except Exception:
        break;
    header=response.headers
    p=response.read()
    if(not header.get_content_charset()=='utf-8'):
        encoding=header.get_content_charset(failobj='utf-8')
        p=p.decode(encoding)
    soup=BeautifulSoup(p,'html.parser',from_encoding='utf-8')
    full_tag_list=soup.select('a.search_result_row.ds_collapse_flag')
    if(len(full_tag_list)==0 or cnt>=100):
        break
    for full_tag in full_tag_list:
        game_name=full_tag.select_one('span.title')
        pure_price=full_tag.select_one('div.col.search_price.discounted.responsive_secondrow')
        if pure_price==None:
            pure_price=soup.select_one('div.col.search_price.responsive_secondrow')
        game_name=game_name.get_text(strip=True)
        game_name=game_name.strip()
        pure_price=pure_price.get_text(strip=True)
        pure_price=pure_price.strip()
        pure_price=pure_price.replace('\n','')
        pure_price=pure_price.replace('\t','')
        pure_price=pure_price.replace(',','')
        pure_price=pure_price.replace(' ','')
        if pure_price.startswith('Free'):
            game_price_map[game_name]=0
        elif pure_price=="":
            continue
        else:
            pure_price=pure_price[1:]
            escape_text=-1
            index=0
            for idx in pure_price:
                if not idx.isdigit():
                    escape_text=index
                    break
                index+=1
            if escape_text>0:
                pure_price=pure_price[:escape_text]
            pure_price=int(pure_price)
            if pure_price <= standard:
                game_price_map[game_name]=pure_price
    cnt+=1
f=open('steamlist.txt','w',encoding='utf-8')
for game,price in game_price_map.items():
    f.write(game+'\n')
f.close()