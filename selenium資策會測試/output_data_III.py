from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import logging
from response import catch_response

def excel_output(driver,url,temp_func):
    source_type = ['移動源 C1','固定燃燒源 C1','工業製程 C1','人為逸散 C1','輸入電力 C2','輸入蒸汽 C2']

    url = url+"/calculate/" 
    for i in source_type:
        if i!='人為逸散 C1' and i!='輸入電力 C2' and i!='輸入蒸汽 C2':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click() 
            time.sleep(1)
            output_func(driver,source_type,temp_func,i,0,0,0,0)

        elif i == '人為逸散 C1':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click() 
            time.sleep(1)
            output_func(driver,source_type,temp_func,i,1,0,0,0)

            driver.get(url+'directFugitiveEmission')      #導回 人為逸散介面
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)
            time.sleep(2)
            output_func(driver,source_type,temp_func,i,2,0,0,0)

            driver.get(url+'directFugitiveEmission')      #導回 人為逸散介面
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)
            time.sleep(2)
            output_func(driver,source_type,temp_func,i,3,0,0,0)
        
        elif i == '輸入電力 C2':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click() 
            time.sleep(1)
            output_func(driver,source_type,temp_func,i,0,1,0,0)

            # driver.get(url+'electricity')  #導回 輸入電力介面
            # element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="綠電 B.3.2.a"]')))
            # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="綠電 B.3.2.a"]')))
            # driver.execute_script("arguments[0].click()", element)
            # output_func(driver,source_type,temp_func,i,0,2,0,0)

        elif i == '輸入蒸汽 C2':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click() 
            time.sleep(1)
            output_func(driver,source_type,temp_func,i,0,0,1,0)

            driver.get(url+'steam')  #導回 蒸氣頁面
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
            driver.execute_script("arguments[0].click()", element)
            output_func(driver,source_type,temp_func,i,0,0,2,0)
        driver.get(url)

    
def output_func(driver,source_type,temp_func,i,rfg_or_fire,elec_or_green,plus_or_minus,ups_or_orther):
    # rfg_or_fire -> 1:workhour 2:RFG 3:Fire
    # elec_or_green -> 1:elec 2:greenelec
    # plus_or_minus -> 1:plus 2:minus
    # 0 : 都不是
    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # 往下滾動至頁面中間
    driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
    time.sleep(1)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '匯入 & 匯出')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '匯入 & 匯出')]")))
    driver.execute_script("arguments[0].click()", element)
    time.sleep(3)

    select = [[rfg_or_fire, '人為逸散 C1(工時計算)','人為逸散 C1(冷媒設備)','人為逸散 C1(消防設備)'], [elec_or_green, '輸入電力 C2(一般用電)'],[plus_or_minus, '輸入蒸氣 C2(加項)','輸入蒸氣 C2(減項)']]
    this_time_select = ''
    for each in select:
        if each[0] > 0:
            this_time_select = each[each[0]]
    
    if temp_func=='output':      #匯出excel資料
        import_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//ul//button[span[text()="匯出"]]')))
        driver.execute_script("arguments[0].click()", import_element)
        time.sleep(5)
        if i!='人為逸散 C1' and i!='輸入電力 C2' and i!='輸入蒸汽 C2' :
            catch_response(driver, i)
        else:
            catch_response(driver, this_time_select)

    elif temp_func =='download':             #單純模板下載
        import_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//ul//button[span[text()="模板下載"]]')))
        driver.execute_script("arguments[0].click()", import_element)
        time.sleep(5)
        # 模板下載沒有response