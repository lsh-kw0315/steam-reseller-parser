import selenium 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

standard=5
if len(sys.argv)>=2:
    if(sys.argv[1].isdigit()):
        standard=int(sys.argv[1])
        
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
for x in range(total_pages):
    if(x>0):
        tmp_url=tmp_url.replace('page={0}'.format(x),'page={0}'.format(x+1))
        driver.get(url=tmp_url)
    full_elements=driver.find_elements(By.CSS_SELECTOR,'div.HitCard.HitCard--dark.faux-block-link')
    scroll=0
    if(len(full_elements)==0):
        break
    for y in full_elements:
        act=ActionChains(driver)
        location=y.location
        driver.execute_script('window.scrollTo({0},{1})'.format(location['x'],location['y']))
        time.sleep(0.5)
        act.move_to_element(y).perform()
        time.sleep(0.5)
        pure_price=y.find_element(By.CSS_SELECTOR,'span.card-price').text
        game_name=y.find_element(By.CSS_SELECTOR,'div.hit-card-game-name>a.faux-block-link__overlay-link').text
        pure_price.strip()
        if(pure_price.startswith("From")):
            pure_price=pure_price[6:]
        else:
            pure_price=pure_price[1:]
        pure_price=float(pure_price)      
        game_name.strip()
        game_price_map[game_name]=pure_price
        scroll+=1
    if(x==0):
        tmp_url=url.format("page=1&")
    
driver.quit()
f=open("fanaticallist.txt","w",encoding='utf-8')
for game,price in game_price_map.items():
    if price <=standard:
        f.write(game+"\n")
f.close();