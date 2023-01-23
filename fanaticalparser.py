import selenium 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import math

standard_price=5
standard_discount=30
if len(sys.argv)>1:
    if(sys.argv[1].isdigit()):
        standard_price=int(sys.argv[1])
if len(sys.argv)>2:
    if(sys.argv[2].isdigit()):
        standard_discount=int(sys.argv[2])

url='https://www.fanatical.com/en/search?{0}types=game%2Cdlc%2Cbundle'
option=webdriver.ChromeOptions()
driver=webdriver.Chrome(executable_path='chromedriver',options=option)
driver.implicitly_wait(time_to_wait=10)
driver.get(url=url.format(""))
total_game_element=driver.find_element(By.CSS_SELECTOR,'span.ais-Stats-text')
total_game_str=total_game_element.text
total_game=int(total_game_str.replace(',',''))
total_pages=total_game//36
if(total_pages==0 or total_pages*36 < total_game):
    total_pages+=1
tmp_url=url.format("")
game_price_map=dict()
game_discount_map=dict()
for x in range(total_pages):
    if(x>0):
        tmp_url=tmp_url.replace('page={0}'.format(x),'page={0}'.format(x+1))
        driver.get(url=tmp_url)
    full_elements=driver.find_elements(By.CSS_SELECTOR,'div.HitCard.HitCard--dark.faux-block-link')
    scroll=0
    if(len(full_elements)==0):
        break
    for full_tag in full_elements:
        act=ActionChains(driver)
        location=full_tag.location
        driver.execute_script('window.scrollTo({0},{1})'.format(location['x'],location['y']))
        act.move_to_element(full_tag).perform()
        time.sleep(0.5)
        sale_price=full_tag.find_element(By.CSS_SELECTOR,'span.card-price').text
        game_name=full_tag.find_element(By.CSS_SELECTOR,'div.hit-card-game-name>a.faux-block-link__overlay-link').text
        sale_price.strip()
        if(sale_price.startswith("From")):
            sale_price=sale_price[6:]
        else:
            sale_price=sale_price[1:]
        sale_price=float(sale_price)      
        game_name.strip()
        
        base_price=None
        try:
            base_price=full_tag.find_element(By.CSS_SELECTOR,'div.was-price')
        except NoSuchElementException as e:
            print('',sep='')
        
        if(base_price==None):
            base_price=sale_price
        else:
            base_price=base_price.text
            base_price=base_price.strip()
            base_price=base_price[1:]
            base_price=float(base_price)
        
        discount=(1-sale_price/base_price)*100
        discount=math.trunc(discount)
        if(sale_price<=standard_price):
            game_price_map[game_name]=sale_price
        if(discount>=standard_discount):
            game_discount_map[game_name]=discount
        scroll+=1
    if(x==0):
        tmp_url=url.format("page=1&")
    
driver.quit()
f1=open("fanatical_price_list.txt","w",encoding='utf-8')
f2=open("fanatical_discount_list.txt",'w',encoding='utf-8')
for game in game_price_map.keys():
    f1.write(game+"\n")
for game in game_discount_map.keys():
    f2.write(game+'\n')
f1.close();
f2.close();
print("task finished.")