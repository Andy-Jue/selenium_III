# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:12:52 2024

@author: iou85
"""

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
from selenium.webdriver.support.ui import Select
import string
from datetime import datetime, timedelta

value_to_send = ['A00', 'A000', 'B00', 'B000', 'C00', 'C000', 'D00', 'D000', 
                 'E00', 'E000', 'F00', 'F000', 'G00', 'G000', 'H00', 'H000', 
                 'I00', 'I000', 'J00', 'J000']



def source_input_1(driver,url):

    source_type = ['人為逸散 C1','其他關注類物質 C1','輸入電力 C2','輸入蒸汽 C2']

    url = url+"/calculate/" 
    
    for i in source_type:
        if i == '人為逸散 C1':
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))
            link.click()
            
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="工時計算 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)
            for j in range(1):
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
                element.click()
                time.sleep(2)
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="請輸入  人員類別"]')))
                element.send_keys("測試人員1")
                time.sleep(2)
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '新增')]")))
                driver.execute_script("arguments[0].click()", element)
                
                time.sleep(0.5)
                workhour(driver,url,j)
            
            

            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)
            time.sleep(3)
            for j in range(1):
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '新增')]")))
                driver.execute_script("arguments[0].click()", element)
    
                time.sleep(0.5)
                input_data(driver, i,j,1)

   
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)
            time.sleep(3)
            for j in range(1):
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '新增')]")))
                driver.execute_script("arguments[0].click()", element)
    
                time.sleep(0.5)
                input_data(driver, i,j,2)
        elif i == '輸入電力 C2':
                link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))
                link.click()
                time.sleep(3)
                page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
                # 往下滾動至頁面中間
                driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
                time.sleep(3)
                for j in range(1):
                    element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
                    element.click()
                    time.sleep(3)
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="請輸入  電號/用戶編號"]')))
                    element.send_keys("測試人員1")
                    time.sleep(3)
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '新增')]")))
                    driver.execute_script("arguments[0].click()", element)
                    time.sleep(5)
                    elec(driver,url,j)
                    time.sleep(0.5)
                
                
                
                # element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="綠電 B.3.2.a"]')))
                # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="綠電 B.3.2.a"]')))
                # driver.execute_script("arguments[0].click()", element)
    
                # time.sleep(0.5)
                # green_elec(driver,url)
        elif i == '輸入蒸汽 C2':       
                link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))
                link.click()
                time.sleep(2)
                steam(driver,url)
                time.sleep(0.5)
                
                
               
        else:
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))
            link.click()
            for j in range(3):
                element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '新增')]")))
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '新增')]")))
                driver.execute_script("arguments[0].click()", element)
                time.sleep(0.5)
                input_data(driver, i,j,0)
            time.sleep(3)

    driver.get(url)
    
def increment_value(value):
    # 假設每次增量為 +1，這裡是對字串最後一位數字加 1 的範例
    if value[-1].isdigit():  # 確保最後一個字符是數字
        return f"{value[:-1]}{int(value[-1]) + 1}"
    return value  # 如果最後一個不是數字，則不變

def generate_license_plate():
    # 隨機生成三個大寫字母
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    # 隨機生成三個數字
    numbers = ''.join(random.choices('0123456789', k=3))
    # 將字母和數字組合成車牌格式
    license_plate = f"{letters}-{numbers}"
    return license_plate

def Process(driver):
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    button = driver.find_element(By.XPATH, "(//form[@id='validateOnly']//button[@type='button'])[1]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    random_index = 2
    first_cell = driver.find_element(By.XPATH, f"//table//tbody//tr[{random_index}]//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
def equipment(driver):
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    button = driver.find_element(By.XPATH, "(//form[@id='validateOnly']//button[@type='button'])[2]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    random_index = 2
    first_cell = driver.find_element(By.XPATH, f"//table//tbody//tr[{random_index}]//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
def fuel_materials(driver):
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    button = driver.find_element(By.XPATH, "(//form[@id='validateOnly']//button[@type='button'])[3]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    random_index = 3
    first_cell = driver.find_element(By.XPATH, f"//table//tbody//tr[{random_index}]//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
def Process_1(driver):
    button = driver.find_element(By.XPATH, "//button[@class='ant-btn ant-btn-link d-flex align-items-center'][1]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    random_index = 2
    first_cell = driver.find_element(By.XPATH, f"//table//tbody//tr[{random_index}]//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
def equipment_1(driver):
    button = driver.find_element(By.XPATH, "//div[@class='ant-space-item']//button[@class='ant-btn ant-btn-link d-flex align-items-center' and span[contains(text(), '設備表')]]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    first_cell = driver.find_element(By.XPATH, "//table//tbody//tr//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
def equipment_rfg(driver):
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    button = driver.find_element(By.XPATH, "(//form[@id='validateOnly']//button[@type='button'])[2]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    random_index = 2
    first_cell = driver.find_element(By.XPATH, f"//table//tbody//tr[{random_index}]//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
def fuel_materials_rfg(driver):
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    button = driver.find_element(By.XPATH, "(//form[@id='validateOnly']//button[@type='button'])[3]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    random_index = 2
    first_cell = driver.find_element(By.XPATH, f"//table//tbody//tr[{random_index}]//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
def Process_fire(driver):
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    button = driver.find_element(By.XPATH, "(//form[@id='validateOnly']//button[@type='button'])[1]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    first_cell = driver.find_element(By.XPATH, "//table//tbody//tr//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
def equipment_fire(driver):
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    button = driver.find_element(By.XPATH, "(//form[@id='validateOnly']//button[@type='button'])[2]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    first_cell = driver.find_element(By.XPATH, "//table//tbody//tr//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
def fuel_materials_fire(driver):
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    button = driver.find_element(By.XPATH, "(//form[@id='validateOnly']//button[@type='button'])[3]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    random_index = 2
    first_cell = driver.find_element(By.XPATH, f"//table//tbody//tr[{random_index}]//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
def equipment_2(driver):
    button = driver.find_element(By.XPATH, "//div[@class='ant-space-item']//button[@class='ant-btn ant-btn-link d-flex align-items-center' and span[contains(text(), '設備表')]]")
    button.click()
    modal_body_locator = ".ant-modal-body"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, modal_body_locator)))
    random_index = 2
    first_cell = driver.find_element(By.XPATH, f"//table//tbody//tr[{random_index}]//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    
# def increment_value(value):
#     prefix = value[:-2]  # 取前缀部分
#     number = int(value[-2:])  # 取后两位数字并转换为整数
#     number += 1  # 增加1
#     return f"{prefix}{str(number).zfill(2)}"

    
    
def input_data(driver, source_type,index,rfg_or_fire):
    # random_letters = ''.join(random.choices(string.ascii_letters, k=10))
    if source_type =='移動源 C1':
        value_to_send[0] = increment_value(value_to_send[0])
        value_to_send[1] = increment_value(value_to_send[1])
        license_plate = generate_license_plate()
        Process(driver)
        equipment(driver)
        fuel_materials(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    
        form_element = driver.find_element(By.ID, "validateOnly")               #表單element
    
        input_elements = form_element.find_elements(By.TAG_NAME, "input")       #tag_name是input的
        
        
        new_inputelements =[]
    
        for i in input_elements:                     #把disable的先移除掉
            # print(i.get_attribute("disable"))
            if i.get_attribute("disabled") != None and i.get_attribute("id")!="validateOnly_referenceFile" and i.get_attribute("type")!="search":#上傳表單與是否屬生質能源
                continue
            else:
                new_inputelements.append(i)
        for input_element in new_inputelements:
            if input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ProcessInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[0])
                time.sleep(0.5)
    
            
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[1])
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_ProductModel":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( license_plate)
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_OriScalar":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(str(100)) #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            # elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_DistributionRatioNumber":
            #     input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            #     input_element.send_keys(Keys.BACKSPACE)      #刪除
            #     input_element.send_keys(str(random.randint(1, 100)))
            #     time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ResponsibleUnit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("不想上班") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_Unit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("id") == 'validateOnly_ingredientName':
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("(逸散)其他") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
    
            elif input_element.get_attribute("placeholder") == "請輸入數字":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(str(12))
                time.sleep(0.5)
            
            elif input_element.get_attribute("placeholder") == "請輸入活動強度單位":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg")
                
            elif input_element.get_attribute("type")=="search":   #選單類 先click 再選 再click
        
                if input_element.get_attribute("id")=="validateOnly_IsBiomassEnergy":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//div[@label="否"]')))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_IsCogenerationEquipment":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '(//div[@label="否"])[2]')))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_Area":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'台灣')]")))
                    element.click()
                    time.sleep(0.5)
                    try:
                        element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[8]')))
                        element.click()
                        # time.sleep(0.5)
                    except:
                        try:
                            element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[7]')))
                            element.click()
                            time.sleep(0.5)
                        except:
                            element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[6]')))
                            element.click()
                            # time.sleep(0.5)
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2023')]")))
                    element.click()
                    # time.sleep(0.5)
                  
                    
                elif input_element.get_attribute("id")=="validateOnly_activityDataType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自動連續')]")))
                    element.click()
                    # time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_emitParaType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自我/量測')]")))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_InstrumentCalibrationSet":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
                    element.click()
                else:
                    continue  
                time.sleep(1)
            

                    
        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))    #送出
        button.click()
        time.sleep(2)
        if rfg_or_fire == 1:
            catch_response(driver,'人為逸散 C1(冷媒設備)')
        elif rfg_or_fire == 2:
            catch_response(driver,'人為逸散 C1(消防設備)')
        else:
            catch_response(driver, source_type)
        time.sleep(2)
    elif  source_type =='固定燃燒源 C1':
        value_to_send[2] = increment_value(value_to_send[2])
        value_to_send[3] = increment_value(value_to_send[3])
        license_plate = generate_license_plate()
        time.sleep(0.5)
        Process(driver)
        time.sleep(0.5)
        equipment(driver)
        fuel_materials(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    
        form_element = driver.find_element(By.ID, "validateOnly")               #表單element
    
        input_elements = form_element.find_elements(By.TAG_NAME, "input")       #tag_name是input的
        
        
        new_inputelements =[]
    
        for i in input_elements:                     #把disable的先移除掉
            # print(i.get_attribute("disable"))
            if i.get_attribute("disabled") != None and i.get_attribute("id")!="validateOnly_referenceFile" and i.get_attribute("type")!="search":#上傳表單與是否屬生質能源
                continue
            else:
                new_inputelements.append(i)
        for input_element in new_inputelements:
            if input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ProcessInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[2])
                time.sleep(0.5)
    
            
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[3])
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_ProductModel":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( license_plate)
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_OriScalar":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( str(100)) #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            # elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_DistributionRatioNumber":
            #     input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            #     input_element.send_keys(Keys.BACKSPACE)      #刪除
            #     input_element.send_keys(str(random.randint(1, 100)))
            #     time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ResponsibleUnit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("不想上班") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_Unit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("id") == 'validateOnly_ingredientName':
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("(逸散)其他") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
    
            elif input_element.get_attribute("placeholder") == "請輸入數字":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(str(12))
                time.sleep(0.5)
            
            elif input_element.get_attribute("placeholder") == "請輸入活動強度單位":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg")
                
            elif input_element.get_attribute("type")=="search":   #選單類 先click 再選 再click
        
                if input_element.get_attribute("id")=="validateOnly_IsBiomassEnergy":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//div[@label="否"]')))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_IsCogenerationEquipment":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '(//div[@label="否"])[2]')))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_Area":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'台灣')]")))
                    element.click()
                    time.sleep(0.5)
                    try:
                        element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[8]')))
                        element.click()
                        # time.sleep(0.5)
                    except:
                        try:
                            element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[7]')))
                            element.click()
                            time.sleep(0.5)
                        except:
                            element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[6]')))
                            element.click()
                            # time.sleep(0.5)
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2023')]")))
                    element.click()
                    # time.sleep(0.5)
                  
                    
                elif input_element.get_attribute("id")=="validateOnly_activityDataType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自動連續')]")))
                    element.click()
                    # time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_emitParaType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自我/量測')]")))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_InstrumentCalibrationSet":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
                    element.click()
                else:
                    continue  
                time.sleep(1)
            

                    
        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))    #送出
        button.click()
        time.sleep(2)
        if rfg_or_fire == 1:
            catch_response(driver,'人為逸散 C1(冷媒設備)')
        elif rfg_or_fire == 2:
            catch_response(driver,'人為逸散 C1(消防設備)')
        else:
            catch_response(driver, source_type)
        time.sleep(2)
    elif  source_type =='工業製程 C1':
        value_to_send[4] = increment_value(value_to_send[4])
        value_to_send[5] = increment_value(value_to_send[5])
        license_plate = generate_license_plate()
        Process(driver)
        equipment(driver)
        fuel_materials(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    
        form_element = driver.find_element(By.ID, "validateOnly")               #表單element
    
        input_elements = form_element.find_elements(By.TAG_NAME, "input")       #tag_name是input的
        
        
        new_inputelements =[]
    
        for i in input_elements:                     #把disable的先移除掉
            # print(i.get_attribute("disable"))
            if i.get_attribute("disabled") != None and i.get_attribute("id")!="validateOnly_referenceFile" and i.get_attribute("type")!="search":#上傳表單與是否屬生質能源
                print("")
            else:
                new_inputelements.append(i)
        for input_element in new_inputelements:
            if input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ProcessInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[4])
                time.sleep(0.5)
    
            
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[5])
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_ProductModel":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( license_plate)
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_OriScalar":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( str(100)) #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            # elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_DistributionRatioNumber":
            #     input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            #     input_element.send_keys(Keys.BACKSPACE)      #刪除
            #     input_element.send_keys(str(random.randint(1, 100)))
            #     time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ResponsibleUnit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("不想上班") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_Unit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("id") == 'validateOnly_ingredientName':
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("(逸散)其他") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
    
            elif input_element.get_attribute("placeholder") == "請輸入數字":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(str(12))
                time.sleep(0.5)
            
            elif input_element.get_attribute("placeholder") == "請輸入活動強度單位":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg")
                
            elif input_element.get_attribute("type")=="search":   #選單類 先click 再選 再click
        
                if input_element.get_attribute("id")=="validateOnly_IsBiomassEnergy":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//div[@label="否"]')))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_IsCogenerationEquipment":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '(//div[@label="否"])[2]')))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_ProccessDescription":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'水泥製程')]")))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_Area":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'台灣')]")))
                    element.click()
                    time.sleep(0.5)
                    try:
                        element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[8]')))
                        element.click()
                        # time.sleep(0.5)
                    except:
                        try:
                            element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[7]')))
                            element.click()
                            time.sleep(0.5)
                        except:
                            element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[6]')))
                            element.click()
                            # time.sleep(0.5)
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2023')]")))
                    element.click()
                    # time.sleep(0.5)
                  
                    
                elif input_element.get_attribute("id")=="validateOnly_activityDataType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自動連續')]")))
                    element.click()
                    # time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_emitParaType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自我/量測')]")))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_InstrumentCalibrationSet":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
                    element.click()
                else:
                    continue  
                time.sleep(1)
            

                    
        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))    #送出
        button.click()
        time.sleep(2)
        if rfg_or_fire == 1:
            catch_response(driver,'人為逸散 C1(冷媒設備)')
        elif rfg_or_fire == 2:
            catch_response(driver,'人為逸散 C1(消防設備)')
        else:
            catch_response(driver, source_type)
        time.sleep(2)
    elif  rfg_or_fire == 1:
        value_to_send[8] = increment_value(value_to_send[8])
        value_to_send[9] = increment_value(value_to_send[9])
        license_plate = generate_license_plate()
        Process(driver)
        equipment_rfg(driver)
        fuel_materials_rfg(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    
        form_element = driver.find_element(By.ID, "validateOnly")               #表單element
    
        input_elements = form_element.find_elements(By.TAG_NAME, "input")       #tag_name是input的
        
        
        new_inputelements =[]
    
        for i in input_elements:                     #把disable的先移除掉
            # print(i.get_attribute("disable"))
            if i.get_attribute("disabled") != None and i.get_attribute("id")!="validateOnly_referenceFile" and i.get_attribute("type")!="search":#上傳表單與是否屬生質能源
                print("")
            else:
                new_inputelements.append(i)
        for input_element in new_inputelements:
            if input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ProcessInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[8])
                time.sleep(0.5)
    
            
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[9])
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_ProductModel":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(license_plate)
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_OriScalar":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(str(100)) #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            # elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_DistributionRatioNumber":
            #     input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            #     input_element.send_keys(Keys.BACKSPACE)      #刪除
            #     input_element.send_keys(str(random.randint(1, 100)))
            #     time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ResponsibleUnit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("不想上班") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_Unit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("id") == 'validateOnly_ingredientName':
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("(逸散)其他") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
    
            elif input_element.get_attribute("placeholder") == "請輸入數字":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(str(100))
                time.sleep(0.5)
            
            elif input_element.get_attribute("placeholder") == "請輸入活動強度單位":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg")
                
            elif input_element.get_attribute("type")=="search":   #選單類 先click 再選 再click
        
                if input_element.get_attribute("id")=="validateOnly_IsBiomassEnergy":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//div[@label="否"]')))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_IsCogenerationEquipment":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '(//div[@label="否"])[2]')))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_ProccessDescription":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'水泥製程')]")))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_EmissionDescription":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'溶劑噴霧劑及冷媒排放源')]")))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_activityDataType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自動連續')]")))
                    element.click()
                    # time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_emitParaType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自我/量測')]")))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_InstrumentCalibrationSet":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
                    element.click()
                else:
                    continue  
                time.sleep(1)
        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))    #送出
        button.click()
        time.sleep(2)

        if rfg_or_fire == 1:
            catch_response(driver,'人為逸散 C1(冷媒設備)')
        elif rfg_or_fire == 2:
            catch_response(driver,'人為逸散 C1(消防設備)')
        elif rfg_or_fire == 3:
            catch_response(driver, '輸入能源上游排放 C4(輸入電力上游)')
        elif rfg_or_fire == 4:
            catch_response(driver, '輸入能源上游排放 C4(其他輸入能源上游)')
        else:
            catch_response(driver, source_type)
        time.sleep(2)
    elif  rfg_or_fire == 2:
        value_to_send[10] = increment_value(value_to_send[10])
        value_to_send[11] = increment_value(value_to_send[11])
        license_plate = generate_license_plate()
        Process_fire(driver)
        equipment_fire(driver)
        fuel_materials_fire(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    
        form_element = driver.find_element(By.ID, "validateOnly")               #表單element
    
        input_elements = form_element.find_elements(By.TAG_NAME, "input")       #tag_name是input的
        
        
        new_inputelements =[]
    
        for i in input_elements:                     #把disable的先移除掉
            # print(i.get_attribute("disable"))
            if i.get_attribute("disabled") != None and i.get_attribute("id")!="validateOnly_referenceFile" and i.get_attribute("type")!="search":#上傳表單與是否屬生質能源
                print("")
            else:
                new_inputelements.append(i)
        for input_element in new_inputelements:
            if input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ProcessInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[10])
                time.sleep(0.5)
    
            
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[11])
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_ProductModel":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(license_plate)
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_OriScalar":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( ''.join(random.choices(string.digits, k=4))) #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            # elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_DistributionRatioNumber":
            #     input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            #     input_element.send_keys(Keys.BACKSPACE)      #刪除
            #     input_element.send_keys(str(random.randint(1, 100)))
            #     time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ResponsibleUnit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("不想上班") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_Unit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("id") == 'validateOnly_ingredientName':
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("(逸散)其他") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
    
            elif input_element.get_attribute("placeholder") == "請輸入數字":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(str(12))
                time.sleep(0.5)
            
            elif input_element.get_attribute("placeholder") == "請輸入活動強度單位":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg")
                
            elif input_element.get_attribute("type")=="search":   #選單類 先click 再選 再click
        
                if input_element.get_attribute("id")=="validateOnly_IsBiomassEnergy":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//div[@label="否"]')))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_IsCogenerationEquipment":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '(//div[@label="否"])[2]')))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_ProccessDescription":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'水泥製程')]")))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_EmissionDescription":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'溶劑噴霧劑及冷媒排放源')]")))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_activityDataType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自動連續')]")))
                    element.click()
                    # time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_emitParaType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自我/量測')]")))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_InstrumentCalibrationSet":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
                    element.click()
                else:
                    continue  
                time.sleep(1)
        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))    #送出
        button.click()
        time.sleep(2)
        if rfg_or_fire == 1:
            catch_response(driver,'人為逸散 C1(冷媒設備)')
        elif rfg_or_fire == 2:
            catch_response(driver,'人為逸散 C1(消防設備)')
        else:
            catch_response(driver, source_type)
        time.sleep(2)
    elif source_type =='其他關注類物質 C1':
        value_to_send[12] = increment_value(value_to_send[12])
        value_to_send[13] = increment_value(value_to_send[13])
        license_plate = generate_license_plate()
        Process(driver)
        equipment(driver)
        fuel_materials_rfg(driver)
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "validateOnly")))
    
        form_element = driver.find_element(By.ID, "validateOnly")               #表單element
    
        input_elements = form_element.find_elements(By.TAG_NAME, "input")       #tag_name是input的
        
        
        new_inputelements =[]
    
        for i in input_elements:                     #把disable的先移除掉
            # print(i.get_attribute("disable"))
            if i.get_attribute("disabled") != None and i.get_attribute("id")!="validateOnly_referenceFile" and i.get_attribute("type")!="search":#上傳表單與是否屬生質能源
                continue
            else:
                new_inputelements.append(i)
        for input_element in new_inputelements:
            if input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ProcessInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(value_to_send[12])
                time.sleep(0.5)
    
            
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_SerialNumber":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send[13])
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_ProductModel":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(license_plate)
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_OriScalar":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( ''.join(random.choices(string.digits, k=4))) #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_DistributionRatioNumber":
                input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
                input_element.send_keys(Keys.BACKSPACE)      #刪除
                input_element.send_keys(str(random.randint(1, 100)))
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ResponsibleUnit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("不想上班") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_Unit":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
            elif input_element.get_attribute("id") == 'validateOnly_ingredientName':
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("(逸散)其他") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                time.sleep(0.5)
    
            elif input_element.get_attribute("placeholder") == "請輸入數字":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(random.randint(1, 100))
                time.sleep(0.5)
            
            elif input_element.get_attribute("placeholder") == "請輸入活動強度單位":
                WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(random.randint(1, 100))
                
            elif input_element.get_attribute("type")=="search":   #選單類 先click 再選 再click
        
                if input_element.get_attribute("id")=="validateOnly_IsBiomassEnergy":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//div[@label="否"]')))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_IsCogenerationEquipment":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '(//div[@label="否"])[2]')))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_ProccessDescription":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'水泥製程')]")))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_EmissionDescription":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'溶劑噴霧劑及冷媒排放源')]")))
                    element.click()
                    time.sleep(0.5)
                elif input_element.get_attribute("id") == 'validateOnly_ingredientName':
                    WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("(逸散)其他") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
                    time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_Area":
                    input_element.click()
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'台灣')]")))
                    element.click()
                    time.sleep(0.5)
                    try:
                        element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[8]')))
                        element.click()
                        # time.sleep(0.5)
                    except:
                        try:
                            element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[7]')))
                            element.click()
                            time.sleep(0.5)
                        except:
                            element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH,  '(//div[@class="ant-cascader-menu-item-content"])[6]')))
                            element.click()
                            # time.sleep(0.5)
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2022')]")))
                    element.click()
                    # time.sleep(0.5)
                elif input_element.get_attribute("id") == "validateOnly_warmGasType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '(逸散)冷媒設備 Refrigerant equipment')]")))
                    element.click()  
                    
                elif input_element.get_attribute("id")=="validateOnly_activityDataType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自動連續')]")))
                    element.click()
                    # time.sleep(0.5)
                elif input_element.get_attribute("id")=="validateOnly_emitParaType":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自我/量測')]")))
                    element.click()
                elif input_element.get_attribute("id")=="validateOnly_InstrumentCalibrationSet":
                    input_element.click()
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
                    element.click()
                else:
                    continue  
                time.sleep(1)
            

                    
        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))    #送出
        button.click()
        time.sleep(2)
        if rfg_or_fire == 1:
            catch_response(driver,'人為逸散 C1(冷媒設備)')
        elif rfg_or_fire == 2:
            catch_response(driver,'人為逸散 C1(消防設備)')
        else:
            catch_response(driver, source_type)
        time.sleep(2)
        
def workhour(driver,url,j):
    value_to_send[6] = increment_value(value_to_send[6])
    value_to_send[7] = increment_value(value_to_send[7])
    
    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
    time.sleep(3)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '編輯')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '編輯')]")))
    driver.execute_script("arguments[0].click()", element)
    Process_1(driver)
    time.sleep(1)
    equipment_1(driver)
    element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="ProcessInformation_SerialNumber"]')
    element.send_keys(value_to_send[6])
    element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="EquipmentInformation_SerialNumber"]')
    element.send_keys(value_to_send[7])
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="EmissionDescription"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '廢水排放源')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自動連續量測')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '製造廠提供')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
    element.click()
    input_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@placeholder="請輸入"]')))
    # 輸入不同的值到每個 <input> 元素
    for i,element in enumerate(input_elements[8:]):
        if i<96:
            value_to_input = random.randint(1, 20)
            element.send_keys(str(100))
        else:
            value_to_input = "下班"
            element.send_keys(value_to_input)
    time.sleep(3) 
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '儲存')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '儲存')]")))
    driver.execute_script("arguments[0].click()", element)
    time.sleep(5)

    catch_response(driver,'人為逸散 C1(工時計算)')
    
def elec(driver,url,index):
    value_to_send[14] = increment_value(value_to_send[14])
    value_to_send[15] = increment_value(value_to_send[15])
    

    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '編輯')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '編輯')]")))
    driver.execute_script("arguments[0].click()", element)

    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-cascader ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-cascader ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'台灣')]")))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2023')]")))
    element.click()
    Process_1(driver)
    time.sleep(1)
    equipment_2(driver)
    element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="ProcessInformation_SerialNumber"]')
    element.send_keys(value_to_send[14] )
    element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="EquipmentInformation_SerialNumber"]')
    element.send_keys(value_to_send[15] )
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自行推估')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '鄰近國家')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '未進行儀器校正或未進行紀錄彙整者')]")))
    element.click()
    
    input_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@placeholder="請輸入"]')))
    # 輸入不同的值到每個 <input> 元素
    for i,element in enumerate(input_elements[8:]):
        if i<78:
            value_to_input = random.randint(1, 20)
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(str(100))
        else:
            value_to_input ="哈哈哈"
            element.send_keys(value_to_input)

    # time.sleep(3)
    # time_out(driver,url)
    time.sleep(2) 
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '儲存')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '儲存')]")))
    driver.execute_script("arguments[0].click()", element)
    time.sleep(5)  #等他儲存完畢
    catch_response(driver,'輸入電力 C2(一般用電)')   #抓response

def green_elec(driver,url):

    time.sleep(1)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '編輯')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '編輯')]")))
    driver.execute_script("arguments[0].click()", element)
    
    input_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//input[@placeholder="請輸入"]'))
    )
    
    # 輸入不同的值到每個 <input> 元素
    for i,element in enumerate(input_elements):
        if i<12:
            value_to_input = random.randint(1, 20)
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(str(100))
        else:
            value_to_input = '下班'
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)

    time.sleep(3) 
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '儲存')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '儲存')]")))
    driver.execute_script("arguments[0].click()", element)
    time.sleep(3)
    catch_response(driver,'輸入電力 C2(綠電)')   #抓response
    
def steam(driver,url):
    time.sleep(5)
    for j in range(1):
        time.sleep(1)
        page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
        # 往下滾動至頁面中間
        driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
        time.sleep(3)
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
        element.click()
    
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="請輸入  蒸氣編號"]')))
        element.send_keys("測試人員1(加項)")
        time.sleep(1)
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '新增')]")))
        driver.execute_script("arguments[0].click()", element)
        time.sleep(5)
        steam_input_1(driver,url,j,0)   #做蒸氣加項
    time.sleep(1)
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
    driver.execute_script("arguments[0].click()", element)
    time.sleep(2)
    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # 往下滾動至頁面中間
    driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
    time.sleep(5)
    for j in range(1):
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
        element.click()
        time.sleep(1)
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="請輸入  蒸氣編號"]')))
        element.send_keys("測試人員1(減項)")
        time.sleep(1)
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '新增')]")))
        driver.execute_script("arguments[0].click()", element)
        time.sleep(5)
        steam_input_2(driver,url,j,1)    #做蒸氣減項

def steam_input_1(driver,url,index,rfg_or_fire):
    value_to_send[16] = increment_value(value_to_send[16])
    value_to_send[17] = increment_value(value_to_send[17])
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '編輯')]")))
    driver.execute_script("arguments[0].click()", element)

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-cascader ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'台灣')]")))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2021')]")))
    element.click()
    Process_1(driver)
    time.sleep(1)
    equipment_2(driver)
    element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="ProcessInformation_SerialNumber"]')
    element.send_keys(value_to_send[16] )
    element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="EquipmentInformation_SerialNumber"]')
    element.send_keys(value_to_send[17] )
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="ElecDescription"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '離網')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '間歇量測')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '國際/資料庫')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行內部校正或經過會計簽證等証明者')]")))
    element.click()
    
    input_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@placeholder="請輸入"]')))
    # 輸入不同的值到每個 <input> 元素
    for i,element in enumerate(input_elements[8:]):
        if i<12:
            value_to_input = random.randint(1, 20)
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(str(100))
        else:
            value_to_input = '下班'
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)
    time.sleep(2) 
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '儲存')]")))
    driver.execute_script("arguments[0].click()", element)    
    time.sleep(3)
    if rfg_or_fire == 0:
        catch_response(driver,'輸入蒸汽 C2(蒸氣加項)')
    elif rfg_or_fire == 1:
        catch_response(driver,'輸入蒸汽 C2(蒸氣減項))')
def steam_input_2(driver,url,index,rfg_or_fire):
    value_to_send[18] = increment_value(value_to_send[18])
    value_to_send[19] = increment_value(value_to_send[19])
    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # 往下滾動至頁面中間
    driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
    time.sleep(2)
    
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '編輯')]")))
    driver.execute_script("arguments[0].click()", element)

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-cascader ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'台灣')]")))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2021')]")))
    element.click()
    Process_1(driver)
    time.sleep(1)
    equipment_2(driver)
    element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="ProcessInformation_SerialNumber"]')
    element.send_keys(value_to_send[18] )
    element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="EquipmentInformation_SerialNumber"]')
    element.send_keys(value_to_send[19] )
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="ElecDescription"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '離網')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '間歇量測')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '國際/資料庫')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行內部校正或經過會計簽證等証明者')]")))
    element.click()
    
    input_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@placeholder="請輸入"]')))
    # 輸入不同的值到每個 <input> 元素
    for i,element in enumerate(input_elements[8:]):
        if i<12:
            value_to_input = random.randint(1, 20)
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(str(100))
        else:
            value_to_input = '下班'
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)
    time.sleep(2) 
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '儲存')]")))
    driver.execute_script("arguments[0].click()", element)    
    time.sleep(5)
    if rfg_or_fire == 0:
        catch_response(driver,'輸入蒸汽 C2(蒸氣加項)')
    elif rfg_or_fire == 1:
        catch_response(driver,'輸入蒸汽 C2(蒸氣減項))')
