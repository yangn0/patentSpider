from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time
import requests
import csv
from xpinyin import Pinyin
import json,os,datetime
import traceback
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


def socksproxy():
    proxyurl = "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=2&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=2&regions="
    r = requests.get(proxyurl)
    proxy = r.text.strip()
    print(proxy)
    return proxy.split(":")




def mk_dir_file(name, PcNum, path='D:\\patent'):

    year = str(datetime.datetime.now().year)
    if datetime.datetime.now().month < 10:
        month = '0'+str(datetime.datetime.now().month)
    else:
        month = str(datetime.datetime.now().month)
    if datetime.datetime.now().day < 10:
        day = '0'+str(datetime.datetime.now().day)
    else:
        day = str(datetime.datetime.now().day)
    if not os.path.exists(os.path.join(path, year)):
        year_path = os.path.join(path, year)
        os.makedirs(year_path)
        path = os.path.join(path, year)
    else:
        path = os.path.join(path, year)
    if not os.path.exists(os.path.join(path, month)):
        month_path = os.path.join(path, month)
        os.makedirs(month_path)
        path = os.path.join(path, month)
    else:
        path = os.path.join(path, month)
    if not os.path.exists(os.path.join(path, day)):
        day_path = os.path.join(path, day)
        os.makedirs(day_path)
        path = os.path.join(path, day)
    else:
        path = os.path.join(path, day)
    p = Pinyin()
    # path_taobao = str(PcNum)+'_pdd_'+p.get_pinyin(name, '')+int(time.time()*100)
    # if not os.path.exists(os.path.join(path, path_pdd)):
    #     path_pdd = os.path.join(path, path_pdd)
    #     os.makedirs(path_pdd)
    #     path = os.path.join(path, path_pdd)
    # else:
    #     path = os.path.join(path, path_pdd) #??????????????????path???????????????
    path = os.path.join(path, "%s_%s_%s_%s.csv" %
                        (pcNum, "patent", p.get_pinyin(name, ""), day))

    return path

def getDriver():
    while 1:
        try:
            # socks=socksproxy()
            # ## ????????????????????????FirefoxProfile??????
            # profile = FirefoxProfile()
            # ## ??????????????????????????????????????????
            # profile.set_preference('network.proxy.type', 1)
            # ## ????????????????????????IP
            # profile.set_preference('network.proxy.http', socks[0])
            # ## ????????????????????????????????????????????????int????????????????????????
            # profile.set_preference('network.proxy.http_port', socks[1])
            # ## ??????????????????htpps????????????????????????
            # profile.set_preference('network.proxy.ssl', socks[0])
            # profile.set_preference('network.proxy.ssl_port', socks[1])
            options = webdriver.FirefoxOptions()
            # options.add_argument("--proxy-server=socks5://"+socksproxy())
            # options.add_experimental_option('excludeSwitches', ['enable-automation'])
            # options.add_argument("--disable-blink-features=AutomationControlled")
            # options.add_argument("--incognito")  # ??????????????????
            # # ????????????
            # options.add_argument('log-level=3')
            driver = webdriver.Firefox(options=options)
            driver.maximize_window()
            # ??????
            # url = "http://epub.sipo.gov.cn/gjcx.jsp?11-01"
            url = "http://epub.sipo.gov.cn/gjcx.jsp?26-05"
            driver.get(url)
            WebDriverWait(driver, 50).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'body > div.main > div > a:nth-child(2)')))
            WebDriverWait(driver, 50).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'body > div.main > table > tbody > tr > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > span:nth-child(5) > input[checked=checked]')))
            driver.execute_script("patas()")
            WebDriverWait(driver, 180).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.cp_box')))
            # ????????????
            driver.execute_script("zl_ft()")
            # ??????
            WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ft_cpdl2')))
            break
        except:
            try:
                driver.quit()
            except:
                pass
            time.sleep(60*3)
            continue
    return driver


def getInfo(driver, href,handle):
    d = dict()
    while 1:
        #handle = driver.current_window_handle
        driver.execute_script(href)
        try:
            handles = driver.window_handles
            driver.switch_to_window(handles[-1])

            title = WebDriverWait(driver, 180).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.xmxx_tit'))).text

            trList = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'body > div.main > div.w287.left > table > tbody > tr > td > table > tbody > tr')))
            infoDict = dict()
            infoDict['???????????????'] = -1
            infoDict['?????????'] = -1
            infoDict['?????????'] = -1
            infoDict['??????????????????'] = -1
            infoDict['?????????'] = -1
            infoDict['LOC Cl.'] = -1
            infoDict['?????????'] = -1
            infoDict['???????????????'] = -1
            infoDict['????????????'] = -1
            infoDict['???????????????']=-1
            infoDict['????????????']=-1
            for tr in trList:
                print(tr.text)
                trSlt = tr.text.split("\u3000")
                infoDict[trSlt[0]] = trSlt[1]
                if trSlt[0]=='?????????':
                    nowTime=time.mktime(time.strptime(trSlt[1],"%Y.%m.%d"))
                    if nowTime>=1622476800:
                        nowTime+=15*365*24*60*60
                    else:
                        nowTime+=10*365*24*60*60
                    infoDict["???????????????"] = time.strftime("%Y.%m.%d", time.localtime(nowTime))

            picList = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ft_cpdl2 a')))
            picUrl = list()
            for pic in picList:
                print(pic.get_attribute("href"))
                picUrl.append(pic.get_attribute("href"))
            try:
                # ????????????
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.cp_botsm > span:nth-child(2) > a:nth-child(1)'))).click()
                handles = driver.window_handles
                driver.switch_to_window(handles[-1])
                trList = WebDriverWait(driver, 180).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.table_flztxx > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr')))
                shiwuList = list()
                for tr in trList:
                    print(tr.text)
                    shiwuList.append(tr.text)
            except:
                pass
            
            if not os.path.exists( os.path.join(dir_path, infoDict['???????????????']) ):
                os.mkdir(os.path.join(dir_path, infoDict['???????????????']))
            pic_path=os.path.join(dir_path, infoDict['???????????????'])
            picSavePath=list()
            for count,pic in enumerate(picUrl):
                while 1:
                    try:
                        image = requests.get(pic)
                        f = open(os.path.join(pic_path,str(count+1)+'.jpg'), 'wb')
                        #???????????????????????????????????????
                        f.write(image.content)
                        f.close()
                        picSavePath.append(os.path.join(pic_path,str(count+1)+'.jpg').split('\\',1)[1])
                        break
                    except Exception as e:
                        print(repr(e))
                        time.sleep(10)
                        continue


            with open(csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([infoDict['???????????????'], title, infoDict['?????????'], infoDict["?????????"], infoDict["??????????????????"], "????????????", "??????????????????", infoDict['?????????'], infoDict['LOC Cl.'],
                                 infoDict["?????????"], infoDict["???????????????"], infoDict["???????????????"], "???????????????????????????", infoDict['????????????'], "???????????????????????????", "????????????????????????", "Docdb??????????????????", infoDict['????????????'],
                                 "page", "????????????", json.dumps(picUrl), json.dumps(picSavePath),json.dumps(infoDict,ensure_ascii=False),json.dumps(shiwuList,ensure_ascii=False)])
            break
        except Exception as e:
            print(repr(e))
            continue
        finally:
            time.sleep(50)
            handles = driver.window_handles
            for h in handles[1:]:
                driver.switch_to_window(h)
                driver.close()
            driver.switch_to_window(handle)
    return 1

if __name__ == "__main__":
    searchPage = 10000 # ????????????
    pcNum = "X1"  # ?????????

    csv_path = mk_dir_file("patent", pcNum,)
    dir_path = os.path.dirname(csv_path)

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["???????????????", "????????????", "?????????", "?????????", "????????????", "????????????", "??????????????????", "?????????", "LOC?????????",
                        "?????????", "?????????", "???????????????", "???????????????????????????", "????????????????????????", "???????????????????????????", "????????????????????????", "Docdb??????????????????", "????????????",
                        "page", "????????????", "image_urls", "picturesavepath"])

    all_href = list()
    driver = getDriver()
    
    for n in range(1, searchPage):
        csv_path = mk_dir_file("patent", pcNum,)
        dir_path = os.path.dirname(csv_path)
        while(1):
            try:
                print(n)
                # ??????
                driver.execute_script("zl_fy(%s)" % n)
                # ??????
                WebDriverWait(driver, 50).until(EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, ".ft_cpdl2:nth-child(9) > dt"), u'%s' % int(n*8)))

                elements = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ft_cpdl2 strong > a')))
                hrefs = list()
                for element in elements:
                    hrefs.append(element.get_attribute("href").split(":")[1])
                print(hrefs)
                handle = driver.current_window_handle
                for href in hrefs:
                    if href in all_href:
                        continue
                    getInfoRtn = getInfo(driver, href,handle)
                    if getInfoRtn == 1:
                        all_href.append(href)
                # driver.quit()
                break
            except:
                try:
                    driver.quit()
                except:
                    pass
                traceback.print_exc()
                time.sleep(60*4)
                driver = getDriver()
                continue

    input()