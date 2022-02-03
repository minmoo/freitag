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
import pyautogui
import schedule


url = 'https://www.freitag.ch/en/f305'
chromedriver = "/usr/src/chrome/chromedriver"

def set_driver():
    # try:
    #     shutil.rmtree(r"C:\chrometemp")  # remove Cookie, Cache files
    # except FileNotFoundError:
    #     pass

    subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    s=Service(f'./{chrome_ver}/chromedriver.exe')
    
    global driver
    try:
        driver = webdriver.Chrome(options=option, service=s)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(options=option, service=s)
        
    driver.implicitly_wait(5)


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def get_new_items():
    # prev items
    with open(f'items.json', 'r') as fp:
        prev_items = json.load(fp)
    
    new_items = []
    for item in driver.find_elements(By.CSS_SELECTOR, '#block-freitag-content > article > section:nth-child(2) > div > div > div > div > div:nth-child(2) > div.container.mx-auto > div > div > div > div.flex.flex-wrap > div:nth-child(n) > div > picture > img'):
        image_src = item.get_attribute('src')
        
        if image_src not in prev_items['imgs']:
            new_items.append(image_src)
            prev_items['imgs'].append(image_src)
            
    
    # curr item 저장
    with open(f'items.json', 'w') as fp:
        json.dump(prev_items, fp)
        
    return new_items


def selenium_action():
    show_more_button = driver.find_element(By.CSS_SELECTOR, '#block-freitag-content > article > section:nth-child(2) > div > div > div > div > div:nth-child(2) > div.container.mx-auto > div > div > a')
    show_more_button.click()
    
    wait = WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#block-freitag-content > article > section:nth-child(2) > div > div > div > div > div:nth-child(2) > div.container.mx-auto > div > div > a > div > span'), 'SHOW LESS'))
    
    new_items = get_new_items(driver)
    
    if(len(new_items) != 0 ):
        telegram_bot.sendMessage(new_items)
    else:
        print("no data")
        
    
def pyautogui_action():
    # click show more button
    pyautogui.moveTo(1000,1350)
    pyautogui.click()
    sleep(3)
    
    new_items = get_new_items()
    
    if(len(new_items) != 0 ):
        telegram_bot.sendMessage(new_items)
    else:
        print("no data")
    
    # refresh
    pyautogui.moveTo(250,110)
    pyautogui.click()
    sleep(5)



def init():
    set_driver()
    driver.get(url)
    
      # cookie button click
    try:
        cookie_button = driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(9) > div > div > div:nth-child(2) > a')
        cookie_button.click()
    except NoSuchElementException:
        pass
    

def main():
    
    init()
    
    # 1. puautogui 방식
    schedule.every(5).minutes.do(pyautogui_action) # 5분마다 실행

    # 2. selenium 방식
    # selenium_action(driver)
    
    while True:
        schedule.run_pending()
        sleep(1)
    

if __name__ == '__main__':
    main()
    
    