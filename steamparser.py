from urllib.request import Request
from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup
from sys import argv
from time import sleep
from pandas import DataFrame

url='https://store.steampowered.com/search/?ignore_preferences=1&category1=998&hidef2p=1&page={}&ndl=1'
standard_price=5000
standard_discount=30
cnt=0
if len(argv)>1:
    if argv[1].isdigit():
        standard_price=int(argv[1])
if len(argv)>2:
    if argv[2].isdigit():
        standard_discount=int(argv[2])
        
game_price_map=dict()
game_discount_map=dict()
url=url.format(cnt);
while(True):
    headers = {'User-Agent': 'Chrome/66.0.3359.181'}
    url=url.replace('page={0}'.format(cnt),'page={0}'.format(cnt+1))
    response=None
    try:
        request=Request(url,headers=headers)
        response=urlopen(request)
    except urllib.error.URLError as e:
        print(e)
        break
    except Exception:
        break;
    header=response.headers
    p=response.read()
    if(not header.get_content_charset()=='utf-8'):
        encoding=header.get_content_charset(failobj='utf-8')
        p=p.decode(encoding)
    soup=BeautifulSoup(p,'html.parser',from_encoding='utf-8')
    #full_tag_list=soup.select('a.search_result_row.ds_collapse_flag.app_impression_tracked')
    full_tag_list=soup.find_all('a',class_='search_result_row ds_collapse_flag')
    if(len(full_tag_list)==0):
        break
    for full_tag in full_tag_list:
        game_name=full_tag.select_one('span.title')
        pure_price=full_tag.select_one('div.col.search_price.discounted.responsive_secondrow')
        discount=full_tag.select_one('div.col.search_discount.responsive_secondrow>span')
        
        if discount==None:
            discount=0
        else:
            discount=discount.text
            discount=discount.strip()
            discount=discount.replace('\n','')
            discount=discount.replace('\t','')
            per_index=discount.find('%')
            discount=discount[1:per_index]
            discount=int(discount)
            
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
        
        
        if(discount>=standard_discount):
            game_discount_map[game_name]=discount
        
        if pure_price.startswith('Free'):
            game_price_map[game_name]=0
        elif pure_price=="":
            continue
        else:
            if(discount==0):
                pure_price=pure_price[1:]
            else:
                won_cnt=0;
                won_idx=0;
                for idx in pure_price:
                    if(not idx.isdigit() and won_cnt==0):
                        won_cnt+=1
                    elif(not idx.isdigit() and won_cnt>0):
                        break
                    won_idx+=1
                pure_price=pure_price[won_idx+1:]
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
            if pure_price <= standard_price:
                game_price_map[game_name]=pure_price
    cnt+=1
    sleep(1)
f1=open('steam_price_list.txt','w',encoding='utf-8')
f2=open('steam_discount_list.txt','w',encoding='utf-8')
df_price=DataFrame.from_dict([game_price_map])
df_discount=DataFrame.from_dict([game_discount_map])
df_price=df_price.melt(var_name='game',value_name='price')
df_discount=df_discount.melt(var_name="game",value_name="discount") 
df_price.to_excel('steam_price_list.xlsx')
df_discount.to_excel('steam_discount_list.xlsx')
for game in game_price_map.keys():
    f1.write(game+'\n')
for game in game_discount_map.keys():
    f2.write(game+'\n')
f1.close()
f2.close()
print("task finished.")