from urllib.request import Request
from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup
from sys import argv
from os import system
from math import trunc
from pandas import DataFrame

def price_formatting(price):
    price=price.replace("\n","")
    price=price.replace("\t","")
    price=price.replace(",","")
    price=price.strip()
    price=price.replace(" ","")
    price=price[1:]
    return int(price)

standard_price=10000
standard_discount=30
if len(argv) > 1:
    if(argv[1].isdigit()):
        standard_price=int(argv[1])
if len(argv)>2:
    if(argv[2].isdigit()):
        standard_discount=int(argv[2])
url = 'https://directg.net/game/game_thumb.html?page={0}{1}{2}{3}'
real_url=None
option_select=None
platform_select=None
genre_select=None
goods_select=None
while(True):
    option_select=input("옵션을 선택하시겠습니까?(0을 입력하면 스킵, 1을 입력하면 옵션 선택):");
    if(option_select.isdigit() and (int(option_select)==0 or int(option_select)==1)):
        option_select=int(option_select)
        break
if(option_select==1):
    
    while(True):
        system('cls')
        print("장르를 설정합니다")
        print("0:설정안함, 2:액션, 3:어드벤처, 4:레이싱/스포츠, 5:롤플레잉, 6:슈팅/FPS, 7:퍼즐, 8:시뮬레이션")
        print("9:기타, 10:전략, 11:액션/RPG 12:액션/어드벤처, 13:스포츠 14:슈팅/액션/RPG, 15:액션/시뮬레이션")
        print("16:전략/시뮬레이션 17:캐주얼 18:리걸 서스펜스 액션")
        genre_select=input("여기에 입력:")
        if(genre_select.isdigit() and (int(genre_select)==0 or (int(genre_select)>=2 and int(genre_select)<=18))):
            genre_select=int(genre_select)
            break
        
    while(True):
        system('cls')
        print("플랫폼을 설정합니다")
        print('0:설정 안함, 에픽게임즈:34, 록스타게임런처:35, 스팀:1, 유비소프트 커넥트:30, 기타:32')
        platform_select=input('여기에 입력:')
        if(platform_select.isdigit()):
            if(int(platform_select)==0 or int(platform_select)==34 or int(platform_select)==35 or int(platform_select)==1 or int(platform_select)==30 or int(platform_select)==32):
                platform_select=int(platform_select)
                break
            
    while(True):
        system('cls')
        print("게임의 유형을 설정합니다")
        print("0:설정 안함, 1:기본 게임, 2:DLC, 3:번들")
        goods_select=input("여기에 입력:")
        if(goods_select.isdigit() and (int(goods_select)>=0 and int(goods_select)<=3)):
            goods_select=int(goods_select)
            break
    genre_form=None
    platform_form=None
    goods_form=None
    
    if(genre_select!=0):
        genre_form="&search_category=%d"%genre_select
    else:
        genre_form=""
        
    if(platform_select!=0):
        platform_form="&search_platform=%d"%platform_select
    else:
        platform_form=""
        
    if(goods_select!=0):
        goods_form="&search_goods_kind=%d"%goods_select
    else:
        goods_form=""
    real_url=url.format(1,genre_form,platform_form,goods_form)
else:
    real_url=url.format(1,"","","")
headers = {'User-Agent': 'Chrome/66.0.3359.181'}
response = None
try:
    # 403 에러를 피하는 용도
    request = Request(real_url, headers=headers)
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
tmp_url=real_url
for x in range(total_page):
    if(x>0):
        tmp_url=tmp_url.replace("page={0}".format(x),"page={0}".format(x+1))
    request=urllib.request.Request(tmp_url,headers=headers)
    response=urllib.request.urlopen(request)
    response_list.append(response);
game_price_map=dict();
game_discount_map=dict()
for response in response_list:
    header=response.headers
    p=response.read()
    if(not (header.get_content_charset()=="utf-8" or header.get_content_charset()=="euc-kr")):
        encoding=header.get_content_charset(failobj='utf-8')
        p=p.decode(encoding)
    soup=BeautifulSoup(p,'html.parser')
    full_tag_list=soup.select("div.product.vm-col.vm-col-3.vertical-separator.col")
    for full_tag in full_tag_list:
        no_sell=full_tag.select_one("span.label.label-primary")
        if(no_sell!=None):
            continue
        else:
            sale_price=full_tag.select_one('span.PricesalesPrice').text
            game_name=full_tag.select_one('div.vm-product-descr-container-1>a>h2').text
            base_price=full_tag.select_one('span.PricebasePrice').text
            game_name=game_name.replace("\n","")
            game_name=game_name.replace("\t","")
            game_name=game_name.strip()
            sale_price=price_formatting(sale_price)
            base_price=price_formatting(base_price)
            discount=(1-sale_price/base_price)*100
            discount=trunc(discount)
            if sale_price<=standard_price:
                game_price_map[game_name]=int(sale_price)
            if discount>=standard_discount:
                game_discount_map[game_name]=int(discount)
f1=open('directg_price_list.txt','w',encoding='utf-8')
f2=open('directg_discount_list.txt','w',encoding='utf-8')
df_price=DataFrame.from_dict([game_price_map])
df_discount=DataFrame.from_dict([game_discount_map])
df_price=df_price.melt(var_name='게임',value_name='가격')
df_discount=df_discount.melt(var_name="게임",value_name="할인율") 
df_price.to_excel('directg_price_list.xlsx')
df_discount.to_excel('directg_discount_list.xlsx')
for name in game_price_map.keys():
    f1.write(name+'\n')
for name in game_discount_map.keys():
   f2.write(name+'\n')
f1.close()
f2.close()
print("task finished.")