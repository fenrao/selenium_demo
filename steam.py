import time
from selenium import webdriver
import xlrd
from datetime import datetime,date
import re
from xlutils.copy import  copy
import os
from  selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.wait import WebDriverWait

exl=xlrd.open_workbook('steam.xls')
wbook=copy(exl)
w_sheet=wbook.get_sheet('Sheet1')
sheet=exl.sheet_by_name('Sheet1')
n=sheet.col_values(0)
p=sheet.col_values(1)


for i in range(154,len(n)):
    print(n[i])
    text=''
    url = 'https://help.steampowered.com/zh-cn/login/'
    steam = {"name":str( n[i]), "ps":str(p[i])}
    chrome = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    try:
     chrome.get(url)
    except TimeoutException as e :
     text='网络超时'

    User = chrome.find_element_by_id("input_username")
    User.send_keys(steam['name'])
    Password = chrome.find_element_by_id('input_password')
    Password.send_keys(steam['ps'])
    chrome.find_element_by_class_name('btnv6_blue_hoverfade').click()
    locator = (By.CLASS_NAME, 'btnv6_blue_hoverfade')
    #WebDriverWait(chrome, 20).until_not(EC.presence_of_element_located(locator))
    #chrome.implicitly_wait(30)
    time.sleep(10)

    try:
        try:
          chrome.find_element_by_link_text("PLAYERUNKNOWN'S BATTLEGROUNDS").click()
          time.sleep(5)
        except TimeoutException as e:
            text='网络错误'
        # locator = (By.LINK_TEXT, "PLAYERUNKNOWN'S BATTLEGROUNDS")
        # WebDriverWait(chrome, 20).until_not(EC.presence_of_element_located(locator))

        #chrome.get('https://help.steampowered.com/zh-cn/wizard/HelpWithGame/?appid=578080')
        #隐式等待

        #chrome.implicitly_wait(30)
        pageSource = chrome.page_source

        if (re.search('记录在案的 VAC 或游戏封禁', pageSource)):
            text='被封禁'
            print('账号被封了')
        elif(re.search('游戏封禁',pageSource)==None):
            text=('可以')
            print('可以')

    except Exception as e:
      time.sleep(3)
      pageSource = chrome.page_source
      if(re.search('您输入的帐户名称或密码错误。',pageSource)):
        text=('密码错误')
        print('密码错误')
      elif (re.search('biyoubar.com', pageSource)):
        print('令牌')

        text=('令牌')

    w_sheet.write(i,7,text)
    os.remove('hao.xls')
    wbook.save('hao.xls')
    chrome.close()
    if(i%100==0):
        time.sleep(20)





