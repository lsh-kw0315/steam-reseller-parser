from urllib.request import Request
from urllib.request import urlopen
import urllib.error
from bs4 import BeautifulSoup
from sys import argv
from os import system
from math import trunc
from pandas import DataFrame
import asyncio
import aiohttp
import time


def price_formatting(price):
    price=price.replace("\n","")
    price=price.replace("\t","")
    price=price.replace(",","")
    price=price.strip()
    return int(price)


async def fetch(session, url):
    headers = {'User-Agent': 'Chrome/66.0.3359.181'}
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def parse_page(html, standard_price, least_price, standard_discount):
    soup = BeautifulSoup(html, 'html.parser')
    full_tag_list = soup.select("div.row.row-cols-1.row-cols-md-1.g-3>div.col")
    
    local_game_price_map = {}
    local_game_discount_map = {}

    for full_tag in full_tag_list:
        game_name_tag = full_tag.select_one('h5.mb-3')
        if not game_name_tag:
            continue
            
        game_name = game_name_tag.text.strip().replace("\n", "").replace("\t", "")
        base_price_tag = full_tag.select_one('s.num.font-11.won')
        sale_price_tag = full_tag.select_one('strong.num.fs-5.fw-bold.text-white.me-2.won')
        sale_ratio_tag = full_tag.select_one('div.rounded-2.bg-primary.font-14.fw-bold.px-3.py-1.me-2.num')

        if not sale_price_tag:
            continue
            
        sale_price = price_formatting(sale_price_tag.text)
        
        base_price = sale_price
        if base_price_tag:
            base_price = price_formatting(base_price_tag.text)

        discount = 0
        if sale_ratio_tag:
            discount = int(sale_ratio_tag.text.replace(" ", "").replace("%", ""))
        elif base_price > 0 and sale_price < base_price:
            discount = trunc((1 - sale_price / base_price) * 100)
        
        if least_price <= sale_price <= standard_price:
            local_game_price_map[game_name] = sale_price
        if discount >= standard_discount:
            local_game_discount_map[game_name] = discount
            
    return local_game_price_map, local_game_discount_map

async def main():
    least_price=500
    standard_price=10000
    standard_discount=30
    if len(argv) > 1:
        if(argv[1].isdigit()):
            standard_price=int(argv[1])
    if len(argv) > 2:
        if(argv[2].isdigit()):
            standard_discount=int(argv[2])
    if len(argv) > 3:
        if(argv[3].isdigit()):
            least_price=int(argv[3])
    url = 'https://directg.net/game/game_list.html?page={0}{1}{2}{3}'
    
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
            print("0:설정안함, 1:액션, 2:RPG, 3:전략, 4:시뮬레이션, 5:스포츠, 6:캐주얼, 7:레이싱")
            print("8:인디, 9:앞서 해보기")
            genre_select=input("여기에 입력:")
            if(genre_select.isdigit() and (int(genre_select)>=0 and int(genre_select)<=9)):
                genre_select=int(genre_select)
                break
        
        while(True):
            system('cls')
            print("플랫폼을 설정합니다")
            print('0:설정 안함, 스팀:1, 에픽 게임즈: 2, 락스타 게임즈:3')
            platform_select=input('여기에 입력:')
            if(platform_select.isdigit()):
                if(int(platform_select)>=0 and int(platform_select)<=3):
                    platform_select=int(platform_select)
                    break
            
        while(True):
            system('cls')
            print("게임의 유형을 설정합니다")
            print("0:설정 안함, 1:기본 게임, 2:DLC, 3:번들, 4: 에디션, 5: 사운드트랙")
            goods_select=input("여기에 입력:")
            if(goods_select.isdigit() and (int(goods_select)>=0 and int(goods_select)<=5)):
                goods_select=int(goods_select)
                break
        genre_form=None
        platform_form=None
        goods_form=None
        
        if(genre_select!=0):
            genre_form="&genre_code=G000%d"%genre_select
        else:
            genre_form=""
        if(platform_select!=0):
            if(platform_select == 2):
                platform_select = 34
            elif(platform_select == 3):
                platform_select = 35
            platform_form="&platform=%d"%platform_select
        else:
            platform_form=""
            
        if(goods_select!=0):
            goods_detail = str()
            if(goods_select == 1):
                goods_detail = "basic"
            elif(goods_select == 2):
                goods_detail = "dlc"
            elif(goods_select == 3):
                goods_detail = "bundle"
            elif(goods_select == 4):
                goods_detail = "edition"
            else:
                goods_detail = "music"
            goods_form="&game_type=%s"%goods_detail
        else:
            goods_form=""
    
        real_url=url.format(1,genre_form,platform_form,goods_form)
    else:
        real_url=url.format(1,"","","")
    
    start_time = time.time()
    print(real_url)
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, real_url)
        soup = BeautifulSoup(html, 'html.parser')
        page_list = soup.select('li.page-item')
        total_page = 0
        for page in page_list:
            if "Last" in page.text and "disabled" not in page.get("class", []):
                url_path = page.findChild("a")["href"]
                start_idx = url_path.find("page=")
                if start_idx == -1: break
                
                end_idx = url_path.find("&", start_idx)
                if end_idx == -1:
                    end_idx = len(url_path)
                
                last_page = int(url_path[start_idx + 5:end_idx])
                total_page = last_page
                break
        
        if total_page == 0:
            total_page = 1
        
        # 모든 페이지에 대한 URL 생성
        urls = []
        base_url = real_url.split('page=')[0]
        options = '&'.join(real_url.split('&')[1:])
        
        for i in range(1, total_page + 1):
            urls.append(f"{base_url}page={i}&{options}")

        tasks = [fetch(session, url) for url in urls]
        pages_html = await asyncio.gather(*tasks)
        
        game_price_map = {}
        game_discount_map = {}
        
        parse_tasks = [parse_page(html, standard_price, least_price, standard_discount) for html in pages_html]
        results = await asyncio.gather(*parse_tasks)

        for price_map, discount_map in results:
            game_price_map.update(price_map)
            game_discount_map.update(discount_map)
    
    end_time = time.time()
    
    print(f"Total time taken: {end_time - start_time} seconds")
    
        # (데이터 저장 부분은 기존 코드와 동일)
    df_price=DataFrame.from_dict([game_price_map]).melt(var_name='게임',value_name='가격')
    df_discount=DataFrame.from_dict([game_discount_map]).melt(var_name="게임",value_name="할인율") 
    df_price.to_excel('directg_price_list.xlsx', index=False)
    df_discount.to_excel('directg_discount_list.xlsx', index=False)
    
    print("task finished.")

if __name__ == '__main__':
    asyncio.run(main())