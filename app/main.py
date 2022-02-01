from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import telegram_bot

from selenium.common.exceptions import NoSuchElementException   
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import shutil

url = 'https://www.freitag.ch/en/f305'
chromedriver = "/usr/src/chrome/chromedriver"

def get_driver():
    # try:
    #     shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
    # except FileNotFoundError:
    #     pass

    subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

    option = Options()
    option.add_argument('--headless')
    option.add_argument('--window-size=1920x1080')
    option.add_argument("--disable-gpu")
    option.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    s=Service(f'./{chrome_ver}/chromedriver.exe')
    try:
        driver = webdriver.Chrome(options=option, service=s)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(options=option, service=s)
        
    driver.implicitly_wait(3)
    return driver


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def get_new_items(driver):
    # prev items
    with open(f'./items.json', 'r') as fp:
        prev_items = json.load(fp)
    
    curr_data ={}
    curr_data['imgs'] = []
    
    new_items = []
    for item in driver.find_elements(By.CSS_SELECTOR, '#block-freitag-content > article > section:nth-child(2) > div > div > div > div > div:nth-child(2) > div.container.mx-auto > div > div > div > div.flex.flex-wrap > div:nth-child(n) > div > picture > img'):
        image_src = item.get_attribute('src')
        curr_data['imgs'].append(image_src)
        
        if image_src not in prev_items['imgs']:
            new_items.append(image_src)
            
    
    # curr item 저장
    with open('./items.json', 'w') as fp:
        json.dump(curr_data, fp)
        
    return new_items
    

def main():
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')    
    # driver = set_chrome_driver()
    driver = get_driver()
    driver.get(url)
    
    # cookie button click
    try:
        cookie_button = driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(9) > div > div > div:nth-child(2) > a')
        cookie_button.click()
    except NoSuchElementException:
        pass
    
    
    show_more_button = driver.find_element(By.CSS_SELECTOR, '#block-freitag-content > article > section:nth-child(2) > div > div > div > div > div:nth-child(2) > div.container.mx-auto > div > div > a')
    show_more_button.click()
    
    wait = WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#block-freitag-content > article > section:nth-child(2) > div > div > div > div > div:nth-child(2) > div.container.mx-auto > div > div > a > div > span'), 'SHOW LESS'))
    
    new_items = get_new_items(driver)
    
    if(len(new_items) != 0 ):
        telegram_bot.sendMessage(new_items)
    
    driver.close()

if __name__ == '__main__':
    main()
    