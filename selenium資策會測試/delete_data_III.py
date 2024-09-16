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

def delete(driver,url):
    source_type = ['移動源 C1','固定燃燒源 C1','工業製程 C1','人為逸散 C1','其他關注類物質 C1','輸入電力 C2','輸入蒸汽 C2']

    filtered_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="pficons"]/a')))
    text_values = []
    
    for element in filtered_elements:
        if element.get_attribute("disabled") != None:
            continue
        else:
            element_text = element.text
            text_values.append(element_text)
    common_texts = set(text_values) & set(source_type)
    text_values = [text for text in text_values if text in common_texts]

    url = url+"/calculate/"  
    for i in source_type:
        if i == '人為逸散 C1':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click()     
            
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="工時計算 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="工時計算 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)
            
            time.sleep(3)
            delete_workhour(driver,url)
            
            driver.get(url+'directFugitiveEmission') 
            
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)

            time.sleep(3)
            delete_data(driver,url,i,1)

            driver.get(url+'directFugitiveEmission') 
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)

            time.sleep(3)
            delete_data(driver,url,i,2)
        elif i =='輸入能源上游排放 C4':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click()
            
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="輸入電力上游 B.5.2.a"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="輸入電力上游 B.5.2.a"]')))
            driver.execute_script("arguments[0].click()", element)

            time.sleep(3)
            delete_data(driver,url,i,0)
            
            driver.get(url+'upstreamEmissions') 
            
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="其他輸入能源上游 B.5.2.a"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="其他輸入能源上游 B.5.2.a"]')))
            driver.execute_script("arguments[0].click()", element)

            time.sleep(3)
            delete_data(driver,url, i,3)
        elif i == '輸入電力 C2' :
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click()
            
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="一般用電 B.3.2.a"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="一般用電 B.3.2.a"]')))
            driver.execute_script("arguments[0].click()", element)
            
            delete_elec(driver,url)
            time.sleep(3)
        elif i == '輸入蒸汽 C2' :
            
            delete_steam(driver,url)
            time.sleep(3)
        else:   
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click()     
            delete_data(driver,url,i,0)
            driver.get(url)


def delete_data(driver,url,i,rfg_or_fire):
    checkbox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.anticon.anticon-delete'))) 
    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.anticon.anticon-delete')))
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(2)
    checkbox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.ant-btn.css-zjzpde.ant-btn-default.ant-btn-dangerous'))) 
    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ant-btn.css-zjzpde.ant-btn-default.ant-btn-dangerous')))
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(3)
    if rfg_or_fire == 1:
        catch_response(driver,'人為逸散 C1(冷媒設備)')
    elif rfg_or_fire == 2:
        catch_response(driver,'人為逸散 C1(消防設備)')
 

def delete_workhour(driver,url):
    driver.get(url+'directFugitiveEmission')
    time.sleep(2) 
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element.click()
    time.sleep(2)
    element = driver.find_element(By.XPATH, '//span[@class="anticon anticon-delete"]')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)
    checkbox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.ant-btn.css-zjzpde.ant-btn-default.ant-btn-dangerous'))) 
    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ant-btn.css-zjzpde.ant-btn-default.ant-btn-dangerous')))
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(3)
    catch_response(driver,'工時計算 C1')
    # driver.quit()

def delete_elec(driver,url):
    driver.get(url+'electricity')
    time.sleep(3) 

    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # 往下滾動至頁面中間
    driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
    
    time.sleep(3)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element.click()
    # driver.execute_script("arguments[0].click();", element)
    time.sleep(2)
    element = driver.find_element(By.XPATH, '//span[@class="anticon anticon-delete"]')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)
    checkbox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.ant-btn.css-zjzpde.ant-btn-default.ant-btn-dangerous'))) 
    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ant-btn.css-zjzpde.ant-btn-default.ant-btn-dangerous')))
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(3)
    catch_response(driver,'輸入電力 C1(一般用電)')
    # driver.quit()
    
def delete_steam(driver,url):
    driver.get(url+'steam')
    bye_steam(driver,url,0)

    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
    driver.execute_script("arguments[0].click()", element)

    bye_steam(driver,url,1)
    

def bye_steam(driver,url,plus_or_minus):
    time.sleep(2)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element.click()
    time.sleep(2)

    element = driver.find_element(By.XPATH, '//span[@class="anticon anticon-delete"]')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)
    checkbox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.ant-btn.css-zjzpde.ant-btn-default.ant-btn-dangerous'))) 
    checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ant-btn.css-zjzpde.ant-btn-default.ant-btn-dangerous')))
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(3)
    if plus_or_minus==0:
        catch_response(driver,'輸入蒸汽 C1(蒸氣加項)')
    else:
        catch_response(driver,'輸入蒸汽 C1(蒸氣減項)')