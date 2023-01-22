from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import sys
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

standard=5
if len(sys.argv)>=2:
    if(sys.argv[1].isdigit()):
        standard=int(sys.argv[1])

url='https://www.indiegala.com/games/all'
options=webdriver.ChromeOptions();
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver=webdriver.Chrome(executable_path='chromedriver',options=options)
driver.get(url)
driver.implicitly_wait(time_to_wait=10)
total_game_element=driver.find_element(By.CSS_SELECTOR,'div.page-link-cont.left')
total_game_str=total_game_element.text
total_game_str=total_game_str.split(" ")[0]
total_game=int(total_game_str)

total_pages=total_game//36
if(total_pages==0 or total_pages*36<total_game):
    total_pages+=1
game_price_map=dict()
for x in range(total_pages):
    wait=WebDriverWait(driver,60)
    element=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'section.browse-default-browse-main-container.default-main-container.main-container')))    
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    full_tags=soup.select("div.main-list-item-col.left")
    if(len(full_tags)==0):
        break
    for i in full_tags:
        game_name_tag=i.select_one('span.product-title-span')
        pure_price_tag=None
        if(i.select_one('div.double-price.right')==None):
            pure_price_tag=i.select_one('div.price.right')
        else:
            pure_price_tag=i.select_one('div.current-price')
        game_name=game_name_tag.text
        pure_price=pure_price_tag.text
        
        game_name=game_name.strip()
        
        pure_price=pure_price.strip()
        pure_price=pure_price[1:]
        
        game_price_map[game_name]=float(pure_price)
    if x==0:
        next_button=driver.find_element(By.CSS_SELECTOR,'a.prev-next')
        next_button.send_keys(Keys.ENTER)
    else:
        buttons=driver.find_elements(By.CSS_SELECTOR,'a.prev-next')
        next_button=buttons[2]
        next_button.send_keys(Keys.ENTER)
    time.sleep(3)
driver.quit()

f=open('indiegalalist.txt','w',encoding='utf-8')
for game,price in game_price_map.items():
    if price <= standard:
        f.write(game+"\n")
f.close()
print("task finished.")
