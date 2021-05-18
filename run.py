from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")  # 配置隐私模式
# 减少打印
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)
driver.maximize_window()
with open('stealth.min.js') as f:
    js = f.read()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})

url="http://epub.sipo.gov.cn/gjcx.jsp?26-05"

driver.get(url)

WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.main > div > a:nth-child(2)')))
time.sleep(3)
driver.execute_script("patas()")

# try:
#     title=WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.cp_box h1')))
# except:
#     title=-1

# href=WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.cp_linr > p > span')))
# try:
#     attr=WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.cp_linr > ul')))
# except:
#     attr=-1

# driver.execute_script("pam3('pip','CN103388778A','0');")
input()