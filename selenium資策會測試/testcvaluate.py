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



def value_test_2(driver,url):
    source_type = ['移動源 C1']
    test_source = ['mobileCombustion']

    url = url+"/calculate/" 
    for i , j in zip(source_type,test_source):
        if j == 'mobileCombustion' or j == 'stationaryCombustion' or j == 'directProcessEmission' :
            temp = url+j
            driver.get(temp)
            time.sleep(2)
            output_data = calculate_co2_mobileCombustion(driver)
            
        #計算Co2
            

            
def calculate_co2_mobileCombustion(driver):
    output_data = []
    total_carbon_emissions = 0
    
    has_next_page = True
    
    while has_next_page :
        table = driver.find_element(By.TAG_NAME, 'table')
        thead_row = table.find_element(By.XPATH, './/thead/tr')
        biomass_energy_index = -1
        activity_data_index = -1
        percentage_index = -1
        Emission_coefficient_index = -1
        carbon_emissions_index = -1
        header_cells = thead_row.find_elements(By.TAG_NAME, 'th')
        for i, cell in enumerate(header_cells):
            if cell.text == '是否屬生質能源':
               biomass_energy_index = i
            elif cell.text =="活動數據":
                activity_data_index = i
            elif cell.text == "活動數據分配比率(%)":
                percentage_index = i
            elif cell.text == "排放係數":
                Emission_coefficient_index = i
            elif cell.text == "碳排放量(kgCO2e)":
                carbon_emissions_index = i
        if biomass_energy_index != -1 and activity_data_index != -1 and percentage_index != -1 and Emission_coefficient_index != -1 and carbon_emissions_index != -1:
            # print(biomass_energy_index,",",activity_data_index,",",percentage_index,",",Emission_coefficient_index,",",carbon_emissions_index)
            # 定位所有的 <tbody> 元素
            tbodies = table.find_elements(By.TAG_NAME, 'tbody')

            for tbody in tbodies:
                rows = tbody.find_elements(By.TAG_NAME, 'tr')
                for row_index, row in enumerate(rows[1:], start=1):
                    biomass_energy_element = row.find_element(By.XPATH, f'.//td[{biomass_energy_index + 1}]')
                    activity_data_element = row.find_element(By.XPATH, f'.//td[{activity_data_index + 1}]')
                    percentage_element = row.find_element(By.XPATH, f'.//td[{percentage_index + 1}]')
                    Emission_coefficient_element = row.find_element(By.XPATH, f'.//td[{Emission_coefficient_index + 1}]')
                    carbon_emissions_element = row.find_element(By.XPATH, f'.//td[{carbon_emissions_index + 1}]')
                    
                   
                    # print(f"Row {row_index}: 是否為生質能源 - {biomass_energy_element.text}, 活動數據 - {activity_data_element.text}, 活動數據分配比率(%) - {percentage_element.text}, 排放係數 - {Emission_coefficient_element.text}, 碳排放量 - {carbon_emissions_element.text}")
                    row_data = {
                        'row_index': row_index,
                        'biomass_energy': biomass_energy_element.text,
                        'activity_data': activity_data_element.text,
                        'percentage': percentage_element.text,
                        'Emission_coefficient': Emission_coefficient_element.text,
                        'carbon_emissions': carbon_emissions_element.text
                    }
                    output_data.append(row_data)
                    # print(f"Row {row_data['row_index']}: 是否為生質能源 - {row_data['biomass_energy']}, 活動數據 - {row_data['activity_data']}, 活動數據分配比率(%) - {row_data['percentage']}, 排放係數 - {row_data['Emission_coefficient']}, 碳排放量 - {row_data['carbon_emissions']}")

    return output_data
    print(output_data)
    
              
                    
           

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
        # 定位 <tbody> 元素
        tbody = table.find_element(By.TAG_NAME, 'tbody')

        # 定位所有的行元素
        rows = tbody.find_elements(By.TAG_NAME, 'tr')

        # 創建一個字典來跟踪每個排放源的排放量總和
        # emissions_dict = {}
        total_emissions_elements = 0

        # 遍歷每個行元素
        row_end = rows[-1]
        
        emissions_elements = row_end.find_element(By.XPATH, f'.//td[{emissions_index - 1}]')
        emissions_element = float(emissions_elements.text)
            
        total_emissions_elements += emissions_element

            
             

            # 獲取排放源和排放量的值
        # emissions = float(emissions_element.text)
        
        

        # 更新排放源的排放量總和
        print(f'排放量 KgCO2e : {total_emissions_elements}')
    else:
        print('未找到標題為 "排放量 KgCO2e" 的列')

    return total_emissions_elements