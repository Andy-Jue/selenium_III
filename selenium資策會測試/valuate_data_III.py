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

def value_test(driver,url):
    source_type = ['移動源 C1','固定燃燒源 C1','工業製程 C1','人為逸散 C1','輸入電力 C2','輸入蒸氣 C2']
    test_source = ['mobileCombustion','stationaryCombustion','directProcessEmission','directFugitiveEmission','electricity','steam']

    url = url+"/calculate/" 
    for i , j in zip(source_type,test_source):
        if j == 'mobileCombustion' or j == 'stationaryCombustion' or j == 'directProcessEmission' :
            temp = url+j
            driver.get(temp)
            time.sleep(2)
            print(i+ " 的 CO2排放量") 
            total_co2 = calculate_co2_mobileCombustion(driver)         #計算Co2
            print(i+ " 的驗證 CO2排放量")
            co2_validate = validate_co2_mobileCombustion(driver)
            if f"{total_co2:.2f}" == f"{co2_validate:.2f}":
                print("CO2驗證正確!!!")
            else:
                print("CO2驗證錯誤!!!")
            print('\n')
        elif j == 'directFugitiveEmission' :
            temp = url+j
            driver.get(temp)
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
            element.click()
            element1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="ant-select-item-option-content"][1]')))
            element1.click()
            
            time.sleep(2)
            print("工時計算 B.2.2.d 的 CO2排放量") 
            total_co2 = calculate_co2_workhour(driver)        #計算Co2
            print("工時計算 B.2.2.d 的 CO2排放量")
            co2_validate = validate_co2_visitor(driver)
            if f"{total_co2:.2f}" == f"{co2_validate:.2f}" :
                print("CO2驗證正確!!!")
            else:
                print("CO2驗證錯誤!!!")
            print('\n')
            
            temp = url+j
            driver.get(temp)
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)

            time.sleep(2)
            print("冷媒設備 B.2.2.d 的 CO2排放量") 
            total_co2 = calculate_co2_visitor(driver)        #計算Co2
            print("冷媒設備 B.2.2.d 的 CO2排放量")
            co2_validate = validate_co2_visitor(driver)
            if f"{total_co2:.2f}" == f"{co2_validate:.2f}" :
                print("CO2驗證正確!!!")
            else:
                print("CO2驗證錯誤!!!")
            print('\n')
            
            temp = url+j
            driver.get(temp)
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)

            time.sleep(2)
            print("消防設備 B.2.2.d 的 CO2排放量") 
            total_co2 = calculate_co2_visitor(driver)         #計算Co2
            print("消防設備 B.2.2.d 的 CO2排放量")
            co2_validate = validate_co2_visitor(driver)
            if f"{total_co2:.2f}" == f"{co2_validate:.2f}" :
                print("CO2驗證正確!!!")
            else:
                print("CO2驗證錯誤!!!")
            print('\n')
        elif j == 'electricity' :
            temp = url+j
            driver.get(temp)
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="一般用電 B.3.2.a"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="一般用電 B.3.2.a"]')))
            driver.execute_script("arguments[0].click()", element)
            time.sleep(2)
            print("一般用電 B.3.2.a 的 CO2排放量") 
            total_co2 = calculate_co2_workhour(driver)         #計算Co2
            print("一般用電 B.3.2.a 的驗證 CO2排放量")
            co2_validate = validate_co2_mobileCombustion(driver)
            if f"{total_co2:.2f}" == f"{co2_validate:.2f}" :
                print("CO2驗證正確!!!")
            else:
                print("CO2驗證錯誤!!!")
            print('\n')
            
        # elif j == 'otherCompound' :
        #     temp = url+j
        #     driver.get(temp)
        #     time.sleep(2)
        #     print(i+ " 的 CO2排放量") 
        #     total_co2 = calculate_co2_otherCompound(driver)         #計算Co2
        #     print(i+ " 的驗證 CO2排放量")
        #     co2_validate = validate_co2_otherCompound(driver)
        #     if f"{total_co2:.2f}" == f"{co2_validate:.2f}" :
        #         print("CO2驗證正確!!!")
        #     else:
        #         print("CO2驗證錯誤!!!")
        #     print('\n')
        elif j == 'upstreamEmissions' :
            temp = url+j
            driver.get(temp)
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="輸入電力上游 B.5.2.a"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="輸入電力上游 B.5.2.a"]')))
            driver.execute_script("arguments[0].click()", element)
            time.sleep(2)
            print("輸入電力上游 B.5.2.a 的 CO2排放量") 
            total_co2 = calculate_co2_visitor(driver)          #計算Co2
            print("輸入電力上游 B.5.2.a 的驗證 CO2排放量")
            co2_validate = validate_co2_visitor(driver)
            if f"{total_co2:.2f}" == f"{co2_validate:.2f}" :
                print("CO2驗證正確!!!")
            else:
                print("CO2驗證錯誤!!!")
            print('\n')
            
            temp = url+j
            driver.get(temp)
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="其他輸入能源上游 B.5.2.a"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="其他輸入能源上游 B.5.2.a"]')))
            driver.execute_script("arguments[0].click()", element)
            
            time.sleep(2)
            print("其他輸入能源上游 B.5.2.a 的 CO2排放量") 
            total_co2 = calculate_co2_visitor(driver)          #計算Co2
            print("其他輸入能源上游 B.5.2.a 的驗證 CO2排放量")
            co2_validate = validate_co2_visitor(driver)
            if f"{total_co2:.2f}" == f"{co2_validate:.2f}" :
                print("CO2驗證正確!!!")
            else:
                print("CO2驗證錯誤!!!")
            print('\n')
        elif j == 'steam':
            temp = url+j
            driver.get(temp)
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="蒸氣加項 B.3.2.b"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="蒸氣加項 B.3.2.b"]')))
            driver.execute_script("arguments[0].click()", element)
            time.sleep(2)
            print("蒸氣加項 B.3.2.b 的 CO2排放量") 
            total_co2 = calculate_co2_workhour(driver)        #計算Co2
            print("蒸氣加項 B.3.2.b 的 CO2排放量")
            co2_validate = validate_co2_visitor(driver)
            if f"{total_co2:.2f}" == f"{co2_validate:.2f}" :
                print("CO2驗證正確!!!")
            else:
                print("CO2驗證錯誤!!!")
            print('\n')
            
            temp = url+j
            driver.get(temp)
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
            driver.execute_script("arguments[0].click()", element)
            time.sleep(2)
            print("蒸氣減項 B.3.2.b 的 CO2排放量") 
            total_co2 = calculate_co2_workhour(driver)        #計算Co2
            print("蒸氣減項 B.3.2.b 的 CO2排放量")
            co2_validate = validate_co2_visitor(driver)
            if f"{total_co2:.2f}" == f"{co2_validate:.2f}" :
                print("CO2驗證正確!!!")
            else:
                print("CO2驗證錯誤!!!")
            print('\n')
                
        
        else:
            temp = url+j
            driver.get(temp)
            time.sleep(2)
            print(i+ " 的 CO2排放量") 
            total_co2 = calculate_co2_visitor(driver)         #計算Co2
            print(i+ " 的驗證 CO2排放量")
            co2_validate = validate_co2_visitor(driver)
            if f"{total_co2:.2f}" == f"{co2_validate:.2f}" :
                print("CO2驗證正確!!!")
            else:
                print("CO2驗證錯誤!!!")
            print('\n')
        
def calculate_co2_mobileCombustion(driver):
    total_carbon_emissions = 0
    
    has_next_page = True
    
    while has_next_page :
        table = driver.find_element(By.TAG_NAME, 'table')
        thead_row = table.find_element(By.XPATH, './/thead/tr')
        carbon_emissions_index = -1
        header_cells = thead_row.find_elements(By.TAG_NAME, 'th')
        for i, cell in enumerate(header_cells):
            if cell.text == '碳排放量' or cell.text == '排放係數' or cell.text == '排放源' or cell.text == '碳排放量 (kg)':
                carbon_emissions_index = i
# 碳排放量=係數值*活動數據
# 係數值=CO2*GWP(CO2)+CH4*GWP(CH4)+N2O*GWP(N2O) 若為生質能源,則不計算CO2
        if carbon_emissions_index != -1:
            # 定位所有的 <tbody> 元素
            tbodies = table.find_elements(By.TAG_NAME, 'tbody')

            for tbody in tbodies:
                rows = tbody.find_elements(By.TAG_NAME, 'tr')
                for row in rows[1:]:
                    carbon_emissions_elements = row.find_elements(By.XPATH, f'.//td[{carbon_emissions_index + 1}]')
                # 獲取燃料種類和碳排放量的值
                    for carbon_emissions_element in carbon_emissions_elements:
                        carbon_emissions = float(carbon_emissions_element.text)
                        total_carbon_emissions += carbon_emissions

                # 更新燃料種類的碳排放量總和
            try:
                next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@title='下一頁']//button[@class='ant-pagination-item-link']")))
                ActionChains(driver).move_to_element(next_button).click().perform()
                time.sleep(2)
            except Exception as e:
                # print(f"An error occurred: {e}")
                print(f'碳排放量總和：{total_carbon_emissions}')# 輸出每種燃料種類的碳排放量總和
                has_next_page = False
        else:
            print('未找到 "碳排放量"')
    return total_carbon_emissions

def validate_co2_mobileCombustion(driver):
    table = driver.find_element(By.XPATH, '//table[contains(@class, "table table-sm table-bordered text-end")]')
    thead_row = table.find_element(By.XPATH, './/thead/tr')

    # 找到 "排放源" 和 "排放量 kgCO2e" 在表頭中的索引位置
    emissions_index = -1
    header_cells = thead_row.find_elements(By.TAG_NAME, 'th')
    for i, cell in enumerate(header_cells):
        
        if cell.text == '排放量 KgCO2e':
            emissions_index = i
    # 檢查是否找到 "排放源" 和 "排放量 kgCO2e" 的索引位置
    if emissions_index != -1:
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        total_emissions_elements = 0
        row_end = rows[-1]
        
        emissions_elements = row_end.find_element(By.XPATH, f'.//td[{emissions_index - 1}]')
        emissions_element = float(emissions_elements.text)
            
        total_emissions_elements += emissions_element
        print(f'排放量 KgCO2e : {total_emissions_elements}')
    else:
        print('未找到標題為 "排放量 KgCO2e" 的列')

    return total_emissions_elements


def calculate_co2_otherCompound(driver):
    total_otherCompoundn_emissions = 0
    
    has_next_page = True
    
    while has_next_page :
        table = driver.find_element(By.TAG_NAME, 'table')
        thead_row = table.find_element(By.XPATH, './/thead/tr')
        carbon_emissions_index = -1
        header_cells = thead_row.find_elements(By.TAG_NAME, 'th')
        for i, cell in enumerate(header_cells):
            if cell.text == '碳排放量' or cell.text == '排放係數' or cell.text == '排放源' or cell.text == '碳排放量(kg)':
                carbon_emissions_index = i
        if carbon_emissions_index != -1:
            # 定位所有的 <tbody> 元素
            tbodies = table.find_elements(By.TAG_NAME, 'tbody')
            total_otherCompoundn_emissions = 0
            
            for tbody in tbodies:
                rows = tbody.find_elements(By.TAG_NAME, 'tr')
                for row in rows[1:]:
                    carbon_emissions_elements = row.find_elements(By.XPATH, f'.//td[{carbon_emissions_index + 1}]')
    
                    for carbon_emissions_element in carbon_emissions_elements:
                        carbon_emissions = float(carbon_emissions_element.text)
                        
                        total_otherCompoundn_emissions += carbon_emissions 
            try:
                next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@title='下一頁']//button[@class='ant-pagination-item-link']")))
                ActionChains(driver).move_to_element(next_button).click().perform()
                time.sleep(2)
            except Exception as e:
                # print(f"An error occurred: {e}")
                print(f'碳排放量總和：{total_otherCompoundn_emissions}')
                has_next_page = False
        else:
            print('未找到 "碳排放量"')
    return total_otherCompoundn_emissions

def validate_co2_otherCompound(driver):
    table = driver.find_element(By.XPATH, '//table[contains(@class, "table table-sm table-bordered text-end")]')
    thead_row = table.find_element(By.XPATH, './/thead/tr')
    emissions_index = -1
    header_cells = thead_row.find_elements(By.TAG_NAME, 'th')
    for i, cell in enumerate(header_cells):
        
        if cell.text == '排放量 KgCO2e':
            emissions_index = i
    if emissions_index != -1:
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        total_otherCompound_elements = 0
        row_end = rows[-1]
        
        emissions_elements = row_end.find_element(By.XPATH, f'.//td[{emissions_index + 1}]')
        emissions_element = float(emissions_elements.text)
            
        total_otherCompound_elements += emissions_element
        print(f'排放量 KgCO2e : {total_otherCompound_elements}')
    else:
        print('未找到標題為 "排放量 KgCO2e" 的列')

    return total_otherCompound_elements

def calculate_co2_visitor(driver):
    total_visitor_emissions = 0
    has_next_page = True
    while has_next_page :
        table = driver.find_element(By.TAG_NAME, 'table')
        thead_row = table.find_element(By.XPATH, './/thead/tr')
        carbon_emissions_index = -1
        header_cells = thead_row.find_elements(By.TAG_NAME, 'th')
        for i, cell in enumerate(header_cells):
            if cell.text == '碳排放量' or cell.text == '排放係數' or cell.text == '排放源' or cell.text == '碳排放量 (kg)' or cell.text == 'KgCO2e':
                carbon_emissions_index = i

        if carbon_emissions_index != -1:
            tbodies = table.find_elements(By.TAG_NAME, 'tbody')

            for tbody in tbodies:
                rows = tbody.find_elements(By.TAG_NAME, 'tr')
                for row in rows[1:]:
                    carbon_emissions_elements = row.find_elements(By.XPATH, f'.//td[{carbon_emissions_index + 1}]')
                    for carbon_emissions_element in carbon_emissions_elements:
                        carbon_emissions = float(carbon_emissions_element.text)
                        total_visitor_emissions += carbon_emissions
            try:
                next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//li[@title='下一頁']//button[@class='ant-pagination-item-link']")))
                ActionChains(driver).move_to_element(next_button).click().perform()
                time.sleep(2)
                
            except Exception :
                print(f'碳排放量總和：{total_visitor_emissions}')
                has_next_page = False    
        else:
            print('未找到 "碳排放量"')
            break

    return total_visitor_emissions

def validate_co2_visitor(driver):
    table = driver.find_element(By.XPATH, '//table[contains(@class, "table table-sm table-bordered text-end")]')
    thead_row = table.find_element(By.XPATH, './/thead/tr')

    # 找到 "排放源" 和 "排放量 kgCO2e" 在表頭中的索引位置
    emissions_index = -1
    header_cells = thead_row.find_elements(By.TAG_NAME, 'th')
    for i, cell in enumerate(header_cells):
        
        if cell.text == '排放量 KgCO2e':
            emissions_index = i
    if emissions_index != -1:
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        total_emissions_elements = 0
        row_end = rows[-1]
        
        emissions_elements = row_end.find_element(By.XPATH, f'.//td[{emissions_index + 1}]')
        emissions_element = float(emissions_elements.text)
            
        total_emissions_elements += emissions_element
        print(f'排放量 KgCO2e : {total_emissions_elements}')
    else:
        print('未找到標題為 "排放量 KgCO2e" 的列')

    return total_emissions_elements


def calculate_co2_workhour(driver):
    total_visitor_emissions = 0
    table = driver.find_element(By.TAG_NAME, 'table')
    tbody_row = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody_row.find_elements(By.TAG_NAME, 'tr')
    carbon_emissions_index = None
    for row in rows:
        
        header_cells = row.find_elements(By.XPATH, './/td')
        for cell in header_cells:
            if cell.text == 'KgCO2e':
                carbon_emissions_index = row
                 
    if carbon_emissions_index is not None:
        carbon_emissions_elements = carbon_emissions_index.find_elements(By.XPATH, './/td')
        for carbon_emissions_element in carbon_emissions_elements[1:]:
            carbon_emissions = float(carbon_emissions_element.text)
            total_visitor_emissions += carbon_emissions
        print(f'碳排放量總和：{total_visitor_emissions}')

    else:
        print('未找到 "碳排放量"')
           
    return total_visitor_emissions