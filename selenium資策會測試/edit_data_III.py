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
import string

def edit(driver,url):
    source_type = ['輸入電力 C2','輸入蒸汽 C2']
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
            workhour_edit(driver,url)
            
            
            driver.get(url+'directFugitiveEmission') 
            
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="冷媒設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)

            element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[@aria-label="edit"]')))
            driver.execute_script("arguments[0].click();", element)


            time.sleep(3)
            input_data(driver, i,1)

            driver.get(url+'directFugitiveEmission') 
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="消防設備 B.2.2.d"]')))
            driver.execute_script("arguments[0].click()", element)

            element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[@aria-label="edit"]')))
            driver.execute_script("arguments[0].click();", element)


            time.sleep(3)
            input_data(driver, i,2)
        elif i == '輸入電力 C2':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click()
            
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="一般用電 B.3.2.a"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="一般用電 B.3.2.a"]')))
            driver.execute_script("arguments[0].click()", element)
            
            elec_edit(driver,url)
            time.sleep(3)
            
            
            # driver.get(url+'electricity') 
            # element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="綠電 B.3.2.a"]')))
            # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="綠電 B.3.2.a"]')))
            # driver.execute_script("arguments[0].click()", element)

            # time.sleep(3)
            # green_elec(driver,url)
        elif i == '輸入蒸汽 C2':
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click()
            
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="蒸氣加項 B.3.2.b"]')))
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="蒸氣加項 B.3.2.b"]')))
            driver.execute_script("arguments[0].click()", element)
            
            steam_edit(driver,url)
            time.sleep(3)
        else:
            link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, i)))
            link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, i)))  
            link.click()
            
            element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//span[@aria-label="edit"]')))
            driver.execute_script("arguments[0].click();", element)
            
            time.sleep(3)
            
            input_data(driver, i,0)
            
        driver.get(url)
    
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
    random_index = random.randint(2, 101)
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
    random_index = random.randint(2, 101)
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
    random_index = random.randint(2, 10)
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
    random_index = random.randint(2, 101)
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
    random_index = random.randint(2, 17)
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
    random_index = random.randint(2, 10)
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
    random_index = random.randint(2, 20)
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
    random_index = random.randint(2, 101)
    first_cell = driver.find_element(By.XPATH, f"//table//tbody//tr[{random_index}]//td//input[@class='ant-radio-input']")
    time.sleep(2)
    first_cell.click()
    button = driver.find_element(By.XPATH, "//div[@class='ant-modal-footer']//button[@class='ant-btn css-dts6b9 ant-btn-primary']")
    button.click()
    

def input_data(driver, source_type,rfg_or_fire):
    # random_letters = ''.join(random.choices(string.ascii_letters, k=10))
    if source_type =='移動源 C1':
        value_to_send_1 = 'A' + str(1).zfill(2) #使用 zfill() 方法將數字填充為兩位數，例如 1 變為 '01'
        value_to_send_2 = 'A' + str(1).zfill(3)
        license_plate = generate_license_plate()
        Process(driver)
        equipment(driver)
        fuel_materials(driver)
    elif source_type =='固定燃燒源 C1':
        value_to_send_1 = 'B' + str(1).zfill(2) #使用 zfill() 方法將數字填充為兩位數，例如 1 變為 '01'
        value_to_send_2 = 'B' + str(1).zfill(3)
        license_plate = generate_license_plate()
        Process(driver)
        equipment(driver)
        fuel_materials(driver)
    elif source_type =='工業製程 C1':
        value_to_send_1 = 'C' + str(1).zfill(2) #使用 zfill() 方法將數字填充為兩位數，例如 1 變為 '01'
        value_to_send_2 = 'C' + str(1).zfill(3)
        license_plate = generate_license_plate()
        Process(driver)
        equipment(driver)
        fuel_materials(driver)
    elif rfg_or_fire == 1:
        value_to_send_1 = 'E' + str(1).zfill(2) #使用 zfill() 方法將數字填充為兩位數，例如 1 變為 '01'
        value_to_send_2 = 'E' + str(1).zfill(3)
        license_plate = generate_license_plate()
        Process(driver)
        equipment_rfg(driver)
        fuel_materials_rfg(driver)
    elif rfg_or_fire == 2:
        value_to_send_1 = 'F' + str(1).zfill(2) #使用 zfill() 方法將數字填充為兩位數，例如 1 變為 '01'
        value_to_send_2 = 'F' + str(1).zfill(3)
        license_plate = generate_license_plate()
        Process_fire(driver)
        equipment_fire(driver)
        fuel_materials_fire(driver)
    elif source_type =='其他關注類物質 C1':
        value_to_send_1 = 'G' + str(1).zfill(2) #使用 zfill() 方法將數字填充為兩位數，例如 1 變為 '01'
        value_to_send_2 = 'G' + str(1).zfill(3)
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
            print("")
        else:
            new_inputelements.append(i)
    for input_element in new_inputelements:
        # if input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ProcessInformation_SerialNumber":
        #     input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
        #     input_element.send_keys(Keys.BACKSPACE)      #刪除
        #     WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send_1)
        #     time.sleep(0.5)

        
        # elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_SerialNumber":
        #     input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
        #     input_element.send_keys(Keys.BACKSPACE)      #刪除
        #     WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( value_to_send_2)
        #     time.sleep(0.5)
        # elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_EquipmentInformation_ProductModel":
        #     input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
        #     input_element.send_keys(Keys.BACKSPACE)      #刪除
        #     WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( license_plate)
        #     time.sleep(0.5)
        if input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_OriScalar":
            input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            input_element.send_keys(Keys.BACKSPACE)      #刪除
            WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys( ''.join(random.choices(string.digits, k=4))) #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
            time.sleep(0.5)
        elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_DistributionRatioNumber":
            input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            input_element.send_keys(Keys.BACKSPACE)      #刪除
            input_element.send_keys(str(random.randint(1, 100)))
            time.sleep(0.5)
        elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_ResponsibleUnit":
            input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            input_element.send_keys(Keys.BACKSPACE)      #刪除
            WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("不想上班") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
            time.sleep(0.5)
        elif input_element.get_attribute("placeholder") == "請輸入"  and input_element.get_attribute("id") == "validateOnly_Unit":
            input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            input_element.send_keys(Keys.BACKSPACE)      #刪除
            WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("L") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
            time.sleep(0.5)
        elif input_element.get_attribute("id") == 'validateOnly_ingredientName':
            input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            input_element.send_keys(Keys.BACKSPACE)      #刪除
            WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("(逸散)其他類") #目前是生成數字,''.join(random.choices(string.ascii_letters, k=10 生成字母10個
            time.sleep(0.5)

        elif input_element.get_attribute("placeholder") == "請輸入數字":
            input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            input_element.send_keys(Keys.BACKSPACE)      #刪除
            WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys(random.randint(1, 100))
            time.sleep(0.5)
        
        elif input_element.get_attribute("placeholder") == "請輸入活動強度單位":
            input_element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            input_element.send_keys(Keys.BACKSPACE)      #刪除
            WebDriverWait(driver, 5).until(EC.visibility_of(input_element)).send_keys("Kg")
            
        elif input_element.get_attribute("type")=="search":   #選單類 先click 再選 再click

            if input_element.get_attribute("id")=="validateOnly_IsBiomassEnergy":
                actions = ActionChains(driver)
                actions.move_to_element(input_element).click().perform()
                element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//div[@label="否"]')))
                element.click()
            elif input_element.get_attribute("id")=="validateOnly_IsCogenerationEquipment":
                actions.move_to_element(input_element).click().perform()
                element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '(//div[@label="否"])[2]')))
                element.click()
                time.sleep(0.5)
            elif input_element.get_attribute("id")=="validateOnly_EmissionDescription":
                actions.move_to_element(input_element).click().perform()
                element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'溶劑噴霧劑及冷媒排放源')]")))
                element.click()
                time.sleep(0.5)
            
            elif input_element.get_attribute("id")=="validateOnly_ProccessDescription":
                actions.move_to_element(input_element).click().perform()
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
                element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2022')]")))
                element.click()
                # time.sleep(0.5)
              
                
            elif input_element.get_attribute("id")=="validateOnly_activityDataType":
                actions.move_to_element(input_element).click().perform()
                element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自行推估')]")))
                element.click()
                # time.sleep(0.5)
            elif input_element.get_attribute("id")=="validateOnly_emitParaType":
                actions.move_to_element(input_element).click().perform()
                element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自我/量測')]")))
                element.click()
            elif input_element.get_attribute("id")=="validateOnly_InstrumentCalibrationSet":
                actions.move_to_element(input_element).click().perform()
                element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行內部校正或經過會計簽證等証明者')]")))
                element.click()
            elif input_element.get_attribute("id") == "validateOnly_ARnGWPid":
                continue
                # time.sleep(0.5)  
            elif input_element.get_attribute("id") == "validateOnly_Commuting":
                input_element.click()
                element1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="ant-select-item-option-content"][1]')))
                element1.click()     
            elif input_element.get_attribute("id") == "validateOnly_TransportTypeID":
                input_element.click()
                element1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="ant-select-item ant-select-item-option ant-pro-filed-search-select-option "][1]')))
                element1.click()      
            elif input_element.get_attribute("id") == "validateOnly_warmGasType":
                actions.move_to_element(input_element).click().perform()
                element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '(逸散)消防設備 Fire safety equipment')]")))
                element.click()
            
            elif input_element.get_attribute("id") == "validateOnly_ParameterID":
                input_element.click()
                try:
                    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'R-11')]")))
                    element.click()
                except:
                    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'R-123')]")))
                    element.click()
            elif input_element.get_attribute("id") == "validateOnly_ParameterID2":
                input_element.click()
                element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '家用冰箱')]")))
                element.click()
            else:
                continue  
            time.sleep(1)
            

                    
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))    #送出
    button.click()
    time.sleep(2.5)
    if rfg_or_fire == 1:
        catch_response(driver,'人為逸散 C1(冷媒設備)')
    elif rfg_or_fire == 2:
        catch_response(driver,'人為逸散 C1(消防設備)')
        catch_response(driver,source_type)
    time.sleep(2)


def workhour_edit(driver,url):
    
    # value_to_send_1 = 'D' + str(1).zfill(2) #使用 zfill() 方法將數字填充為兩位數，例如 1 變為 '01'
    # value_to_send_2 = 'D' + str(1).zfill(3)
    
    actions = ActionChains(driver)
    
    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # 往下滾動至頁面中間
    driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
    time.sleep(1)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '編輯')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '編輯')]")))
    driver.execute_script("arguments[0].click()", element)
    Process_1(driver)
    time.sleep(1)
    equipment_1(driver)
    # element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="ProcessInformation_SerialNumber"]')
    # element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
    # element.send_keys(Keys.BACKSPACE)      #刪除
    # element.send_keys(value_to_send_1)
    # time.sleep(1)
    # element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="EquipmentInformation_SerialNumber"]')
    # element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
    # element.send_keys(Keys.BACKSPACE)      #刪除
    # element.send_keys(value_to_send_2)
    # time.sleep(1)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmissionDescription"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmissionDescription"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '廢水排放源')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自動連續量測')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '製造廠提供')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
    element.click()
    input_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@placeholder="請輸入"]')))
    #num_elements = len(input_elements)
    #print("找到的元素個數為:", num_elements)
    # 輸入不同的值到每個 <input> 元素
    for i,element in enumerate(input_elements[8:]):
        if i<96:
            value_to_input = random.randint(1, 20)
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)
        else:
            value_to_input = "哈哈哈"
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)
    time.sleep(3) 
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '儲存')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '儲存')]")))
    driver.execute_script("arguments[0].click()", element)
    time.sleep(5)

    catch_response(driver,'人為逸散 C1(工時計算)')
    
def elec_edit(driver,url):
    # value_to_send_1 = 'H' + str(1).zfill(2) #使用 zfill() 方法將數字填充為兩位數，例如 1 變為 '01'
    # value_to_send_2 = 'H' + str(1).zfill(3)
    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # 往下滾動至頁面中間
    driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
    time.sleep(3)
    actions = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '編輯')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '編輯')]")))
    driver.execute_script("arguments[0].click()", element)

    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-cascader ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-cascader ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'台灣')]")))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2022')]")))
    element.click()
    Process_1(driver)
    time.sleep(1)
    equipment_2(driver)
    # element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="ProcessInformation_SerialNumber"]')
    # element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
    # element.send_keys(Keys.BACKSPACE)      #刪除
    # element.send_keys(value_to_send_1)
    # element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="EquipmentInformation_SerialNumber"]')
    # element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
    # element.send_keys(Keys.BACKSPACE)      #刪除
    # element.send_keys(value_to_send_2)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '自行推估')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '鄰近國家')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
    element.click()
    
    input_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@placeholder="請輸入"]')))
    # 輸入不同的值到每個 <input> 元素
    for i,element in enumerate(input_elements[8:]):
        if i<78:
            value_to_input = random.randint(1, 20)
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)
        else:
            value_to_input ="哈哈哈"
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)

    # time.sleep(3)
    # time_out(driver,url)
    time.sleep(2) 
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '儲存')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '儲存')]")))
    driver.execute_script("arguments[0].click()", element)
    time.sleep(5)  #等他儲存完畢
    catch_response(driver,'輸入電力 C2(一般用電)')   #抓response

def steam_edit(driver,url):
    driver.get(url+'steam')
    time.sleep(2)
    edit_steam_input_1(driver,url,0)   #做蒸氣加項
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="蒸氣減項 B.3.2.b"]')))
    driver.execute_script("arguments[0].click()", element)
    edit_steam_input_2(driver,url,1)    #做蒸氣減項
    
    


def edit_steam_input_1(driver,url,rfg_or_fire):
    # value_to_send_1 = 'J' + str(1).zfill(2) #使用 zfill() 方法將數字填充為兩位數，例如 1 變為 '01'
    # value_to_send_2 = 'J' + str(1).zfill(3)
    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # 往下滾動至頁面中間
    driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
    time.sleep(3)  
    actions = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '編輯')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '編輯')]")))
    driver.execute_script("arguments[0].click()", element)

    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-cascader ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-cascader ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'台灣')]")))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2021')]")))
    element.click()
    Process_1(driver)
    time.sleep(1)
    equipment_2(driver)
    # element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="ProcessInformation_SerialNumber"]')
    # element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
    # element.send_keys(Keys.BACKSPACE)      #刪除
    # element.send_keys(value_to_send_1)
    # element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="EquipmentInformation_SerialNumber"]')
    # element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
    # element.send_keys(Keys.BACKSPACE)      #刪除
    # element.send_keys(value_to_send_2)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ElecDescription"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ElecDescription"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '離網')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '間歇量測')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '所在區域/國家')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
    element.click()
    
    input_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@placeholder="請輸入"]')))
    # 輸入不同的值到每個 <input> 元素
    for i,element in enumerate(input_elements[8:]):
        if i<12:
            value_to_input = random.randint(1, 20)
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)
        else:
            value_to_input = '哈哈'
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)
    time.sleep(2) 
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '儲存')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '儲存')]")))
    driver.execute_script("arguments[0].click()", element)    
    time.sleep(5)
    if rfg_or_fire == 0:
        catch_response(driver,'輸入蒸汽 C2(蒸氣加項)')
    elif rfg_or_fire == 1:
        catch_response(driver,'輸入蒸汽 C2(蒸氣減項))')
def edit_steam_input_2(driver,url,rfg_or_fire):
    # value_to_send_1 = 'J' + str(1).zfill(2) #使用 zfill() 方法將數字填充為兩位數，例如 1 變為 '01'
    # value_to_send_2 = 'J' + str(1).zfill(3)
    page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # 往下滾動至頁面中間
    driver.execute_script(f"window.scrollTo(0, {page_height // 3});")
    time.sleep(3)
    actions = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '編輯')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '編輯')]")))
    driver.execute_script("arguments[0].click()", element)

    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-cascader ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-cascader ant-select-in-form-item ant-select-single ant-select-show-arrow"]')))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'台灣')]")))
    element.click()
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'2021')]")))
    element.click()
    Process_1(driver)
    time.sleep(1)
    equipment_2(driver)
    # element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="ProcessInformation_SerialNumber"]')
    # element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
    # element.send_keys(Keys.BACKSPACE)      #刪除
    # element.send_keys(value_to_send_1)
    # element = driver.find_element(By.XPATH, '//input[@placeholder="請輸入" and @id="EquipmentInformation_SerialNumber"]')
    # element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
    # element.send_keys(Keys.BACKSPACE)      #刪除
    # element.send_keys(value_to_send_2)
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ElecDescription"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ElecDescription"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '離網')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="ActivityDataType"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '間歇量測')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="EmitParaType"]')))
    element.click()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '所在區域/國家')]")))
    element.click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ant-select ant-select-in-form-item ant-select-status-success ant-select-single ant-select-show-arrow"][@name="InstrumentCalibrationSet"]')))
    actions.move_to_element(element).click().perform()
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '有進行外部校正或有多組數據茲佐證者')]")))
    element.click()
    
    input_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@placeholder="請輸入"]')))
    # 輸入不同的值到每個 <input> 元素
    for i,element in enumerate(input_elements[8:]):
        if i<12:
            value_to_input = random.randint(1, 20)
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)
        else:
            value_to_input = '哈哈'
            element.send_keys(Keys.CONTROL, 'a')   #crtl+A 全選
            element.send_keys(Keys.BACKSPACE)      #刪除
            element.send_keys(value_to_input)
    time.sleep(2) 
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '儲存')]")))
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '儲存')]")))
    driver.execute_script("arguments[0].click()", element)    
    time.sleep(5)
    if rfg_or_fire == 0:
        catch_response(driver,'輸入蒸汽 C2(蒸氣加項)')
    elif rfg_or_fire == 1:
        catch_response(driver,'輸入蒸汽 C2(蒸氣減項))')