import urllib.request
import urllib.response
import urllib.error
import urllib.robotparser
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time


standard=5
if len(sys.argv) >= 2:
    if(sys.argv[1].isdigit()):
        standard=int(sys.argv[1])
url = 'https://www.humblebundle.com/store/search?sort=bestselling&hmb_source=navbar{0}'
real_url=url.format("")
options=webdriver.ChromeOptions();
driver=webdriver.Chrome(executable_path='chromedriver')
driver.implicitly_wait(30)
driver.get(real_url)

total_str=driver.find_element(By.CSS_SELECTOR,'h1.js-title-text').text
total_str=total_str.replace(',','')
total_str=total_str.split(" ")[0]
total=int(total_str)
total_page=total//20;
if total_page==0:
    total_page=1;
if total_page*20<total:
    total_page+=1
tmp_url=real_url
html=driver.page_source
game_price_map=dict()
for x in range(total_page):
    if(x>0):
        tmp_url=tmp_url.replace('page={0}'.format(x),'page={0}'.format(x+1))
        driver.get(tmp_url)
        time.sleep(1)
        html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    full_tags=soup.select('li.entity-block-container.js-entity-container')
    for i in full_tags:
        game_name=i.select_one('span.entity-title').text
        pure_price=i.select_one('span.price').text
        pure_price.strip()
        pure_price=pure_price[3:]
        game_name.strip()
        game_price_map[game_name]=float(pure_price)
    if(x==0):
        tmp_url=url.format("&page=1")
driver.quit()
f=open('humblebundlelist.txt','w',encoding='utf-8')
for game,price in game_price_map.items():
    if price<=standard:
        f.write(game+'\n')    
f.close()
