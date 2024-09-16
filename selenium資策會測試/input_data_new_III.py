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

def excel_input_new(driver,url,site_num):
    source_type = ['移動源 C1','固定燃燒源 C1','工業製程 C1','人為逸散 C1','輸入電力 C2','輸入蒸汽 C2']

    file_path = 'C:\\Users\\iou85\\Desktop\\selenium資策會測試\\excel資策會模板\\'
    upload_path = ['移動源.xlsx','固定源.xlsx','製程.xlsx','工時.xlsx','冷媒.xlsx','消防.xlsx','電力.xlsx','蒸氣.xlsx','蒸氣.xlsx']

                   
    for_response = ['移動源 C1','固定燃燒源 C1','工業製程 C1','人為逸散 C1(工時計算)','人為逸散 C1(冷媒設備)','人為逸散 C1(消防設備)','輸入電力 C2(一般用電)','輸入蒸汽 C2(加項)','輸入蒸汽 C2(減項)']
    #for_response 單純拿來寫response
    url = url+"/calculate/" 
    now=-1          #記第幾個upload_path，因為有冷媒、消防設備
    for i in range(len(source_type)):
        now+=1
        if source_type[i]!='人為逸散 C1' and source_type[i]!='輸入電力 C2' and source_type[i]!='輸入蒸汽 C2':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, source_type[i])))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, source_type[i])))  
            link.click() 
            time.sleep(1)
            excel_import(driver,source_type,file_path,upload_path,url,now,for_response)
            time.sleep(1)
        elif source_type[i]=='人為逸散 C1':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, source_type[i])))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, source_type[i])))  
            link.click() 
            time.sleep(1)
            excel_import(driver,source_type,file_path,upload_path,url,now,for_response)
            driver.get(url+'directFugitiveEmission')      #導回 人為逸散介面
            now+=1
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)
            time.sleep(2)
            excel_import(driver,source_type,file_path,upload_path,url,now,for_response)
            driver.get(url+'directFugitiveEmission')
            now+=1
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)
            excel_import(driver,source_type,file_path,upload_path,url,now,for_response)
            time.sleep(2)
        elif source_type[i]=='輸入電力 C2':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, source_type[i])))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, source_type[i])))  
            link.click() 
            excel_import(driver,source_type,file_path,upload_path,url,now,for_response)
            time.sleep(2)
        elif source_type[i]=='輸入蒸汽 C2':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, source_type[i])))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, source_type[i])))  
            link.click()
            excel_import(driver,source_type,file_path,upload_path,url,now,for_response)
            now+=1
            driver.get(url+'steam')  #導回 蒸氣頁面
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
            driver.execute_script("arguments[0].click()", element)
            excel_import(driver,source_type,file_path,upload_path,url,now,for_response)
            time.sleep(2) 
    driver.quit()

def excel_import(driver,source_type,file_path,upload_path,url,now,for_response):

    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '匯入 & 匯出')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '匯入 & 匯出')]")))
    driver.execute_script("arguments[0].click()", element)
    time.sleep(3)
    import_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//ul//button[span[text()="匯入"]]')))
    driver.execute_script("arguments[0].click()", import_element)
    time.sleep(2)

    file_input = driver.find_element(By.XPATH, '//input[@id="Excel"]')  #上傳檔案(路徑要自己改)
    temp = file_path + upload_path[now]
    file_input.send_keys(temp)
    
    time.sleep(1)
    upload_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='ant-btn ant-btn-primary']")))
    driver.execute_script("arguments[0].click()", upload_element)

    if upload_path[now] not in {'移動源.xlsx','固定源.xlsx','製程.xlsx','工時.xlsx','電力.xlsx','蒸氣.xlsx','蒸氣.xlsx'}:
        print(upload_path[now])
        time.sleep(1)
        save_element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "確 定")]')))
        driver.execute_script("arguments[0].click()", save_element)

        time.sleep(1)
        catch_response(driver,for_response[now])
        

    else:# upload_path[now]=='RFG.xlsx' or upload_path[now]=='Fire.xlsx':
        print(upload_path[now])
        save_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "儲 存")]')))
        driver.execute_script("arguments[0].click()", save_element)
        time.sleep(3)
        catch_response(driver,for_response[now])

    driver.get(url)
    time.sleep(3)