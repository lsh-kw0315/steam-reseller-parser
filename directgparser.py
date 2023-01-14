import urllib.request
import urllib.response
import urllib.error
import urllib.robotparser
from bs4 import BeautifulSoup
import sys
import os


standard=10000
if len(sys.argv) >= 2:
    if(sys.argv[1].isdigit()):
        standard=int(sys.argv[1])
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
        os.system('cls')
        print("장르를 설정합니다")
        print("0:설정안함, 2:액션, 3:어드벤처, 4:레이싱/스포츠, 5:롤플레잉, 6:슈팅/FPS, 7:퍼즐, 8:시뮬레이션")
        print("9:기타, 10:전략, 11:액션/RPG 12:액션/어드벤처, 13:스포츠 14:슈팅/액션/RPG, 15:액션/시뮬레이션")
        print("16:전략/시뮬레이션 17:캐주얼 18:리걸 서스펜스 액션")
        genre_select=input("여기에 입력:")
        if(genre_select.isdigit() and (int(genre_select)==0 or (int(genre_select)>=2 and int(genre_select)<=18))):
            genre_select=int(genre_select)
            break
        
    while(True):
        os.system('cls')
        print("플랫폼을 설정합니다")
        print('0:설정 안함, 에픽게임즈:34, 록스타게임런처:35, 스팀:1, 유비소프트 커넥트:30, 기타:32')
        platform_select=input('여기에 입력:')
        if(platform_select.isdigit()):
            if(int(platform_select)==0 or int(platform_select)==34 or int(platform_select)==35 or int(platform_select)==1 or int(platform_select)==30 or int(platform_select)==32):
                platform_select=int(platform_select)
                break
            
    while(True):
        os.system('cls')
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
    request = urllib.request.Request(real_url, headers=headers)
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
for y in response_list:
    header=y.headers
    p=y.read()
    if(not (header.get_content_charset()=="utf-8" or header.get_content_charset()=="euc-kr")):
        encoding=header.get_content_charset(failobj='utf-8')
        p=p.decode(encoding)
    soup=BeautifulSoup(p,'html.parser')
    full_space_tag=soup.select("div.product.vm-col.vm-col-3.vertical-separator.col")
    pure_price_tag=list()
    game_name_tag=list()
    for z in full_space_tag:
        no_sell=z.select_one("span.label.label-primary")
        if(no_sell!=None):
            continue
        else:
            pure_price_tag.append(z.select_one('span.PricesalesPrice'))
            game_name_tag.append(z.select_one('div.vm-product-descr-container-1>a>h2'))
    for i,j in zip(pure_price_tag,game_name_tag):
        pure_price=i.text
        game_name=j.text
        game_name=game_name.replace("\n","")
        game_name=game_name.replace("\t","")
        game_name=game_name.strip()
        
        pure_price=pure_price.replace("\n","")
        pure_price=pure_price.replace("\t","")
        pure_price=pure_price.replace(",","")
        pure_price=pure_price.strip()
        pure_price=pure_price.replace(" ","")
        pure_price=pure_price[1:]
        game_price_map[game_name]=int(pure_price)
lower_game=list()
for name,price in game_price_map.items():
    if(price<=standard):
        lower_game.append(name)
f=open('list.txt','w')
for text in lower_game:
    f.write(text+'\n')
f.close()