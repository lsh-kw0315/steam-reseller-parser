from selenium import webdriver
from selenium.webdriver.common.by import By
from sys import argv
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from math import trunc
from pandas import DataFrame

standard_price=5
standard_discount=30
if len(argv)>1:
    if(argv[1].isdigit()):
        standard_price=int(argv[1])
if len(argv)>2:
    if(argv[2].isdigit()):
        standard_discount=int(argv[2])

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
game_discount_map=dict()
for x in range(total_pages):
    wait=WebDriverWait(driver,60)
    element=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'section.browse-default-browse-main-container.default-main-container.main-container')))    
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    full_tags=soup.select("div.main-list-item-col.left")
    if(len(full_tags)==0):
        break
    for full_tag in full_tags:
        game_name_tag=full_tag.select_one('span.product-title-span')
        sale_price_tag=full_tag.select_one('div.double-price.right')
        base_price=None
        if(sale_price_tag==None):
            sale_price_tag=full_tag.select_one('div.price.right')
            base_price_tag=full_tag.select_one('div.price.right')
        else:
            sale_price_tag=full_tag.select_one('div.current-price')
            base_price_tag=full_tag.select_one('div.old-price')
        game_name=game_name_tag.text
        sale_price=sale_price_tag.text
        base_price=base_price_tag.text
        
        game_name=game_name.strip()
        
        sale_price=sale_price.strip()
        sale_price=sale_price[1:]
        sale_price=float(sale_price)
        
        base_price=base_price.strip()
        base_price=base_price[1:]
        
        discount=(1-float(sale_price)/float(base_price))*100
        discount=float(discount)
        if sale_price<=standard_price:
            game_price_map[game_name]=float(sale_price)
        if discount>=standard_discount:
            game_discount_map[game_name]=trunc(discount)
    try:   
        if x==0:
            next_button=driver.find_element(By.CSS_SELECTOR,'a.prev-next')
            next_button.send_keys(Keys.ENTER)
        else:
            buttons=driver.find_elements(By.CSS_SELECTOR,'a.prev-next')
            next_button=buttons[2]
            next_button.send_keys(Keys.ENTER)
    except Exception:
        while True:
            if x==0:
                next_button=driver.find_element(By.CSS_SELECTOR,'a.prev-next')
                if next_button !=None:
                    next_button.send_keys(Keys.ENTER)
                    break
            else:
                buttons=driver.find_elements(By.CSS_SELECTOR,'a.prev-next')
                if buttons: 
                    next_button=buttons[2]
                    next_button.send_keys(Keys.ENTER)
                    break
    sleep(0.7)
driver.quit()

f1=open('indiegala_price_list.txt','w',encoding='utf-8')
f2=open('indiegala_discount_list.txt','w',encoding='utf-8')
df_price=DataFrame.from_dict([game_price_map])
df_discount=DataFrame.from_dict([game_discount_map])
df_price=df_price.melt(var_name='game',value_name='price')
df_discount=df_discount.melt(var_name="game",value_name="discount") 
df_price.to_excel('indiegala_price_list.xlsx')
df_discount.to_excel('indiegalas_discount_list.xlsx')
for game,price in game_price_map.items():
    if price <= standard_price:
        f1.write(game+"\n")
for game,discount in game_discount_map.items():
    if discount >= standard_discount:
        f2.write(game+'\n')
f1.close()
f2.close()
print("task finished.")
