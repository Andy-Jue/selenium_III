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
from create_data_III import source_input,input_data
from create_data_III_people import source_input_1
from input_data_old_III import excel_input_old
from input_data_new_III import excel_input_new
from report_valuate_III import value_test
from output_data_III import excel_output
from edit_data_III import edit
from delete_data_III import delete, delete_workhour, delete_elec ,delete_steam
from testcvaluate import value_test_2
# from selenium.webdriver.common.action_chains import ActionChains
def calculate_co2_mobileCombustion(driver):
    try:
        table_body = WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
       )
       
    except:
        print("tbody失敗")

   # 找到目标行 <tr id="w-e-element-494">
    try:
        target_row = WebDriverWait(table_body, 10).until(
            EC.presence_of_element_located((By.XPATH, '//tr[17]'))
        )
    except:
        print("tr失敗")
 
    # 在目标行中找到目标 <span id="w-e-text-496">
    target_span1 = WebDriverWait(target_row, 10).until(
        EC.presence_of_element_located((By.XPATH, './/td[1]'))
    )
    target_span2 = WebDriverWait(target_row, 10).until(
        EC.presence_of_element_located((By.XPATH, './/td[2]'))
    )
    target_span3 = WebDriverWait(target_row, 10).until(
        EC.presence_of_element_located((By.XPATH, './/td[3]'))
    )
    target_span4 = WebDriverWait(target_row, 10).until(
        EC.presence_of_element_located((By.XPATH, './/td[4]'))
    )
    print("固定排放: ",target_span1.text,"製程排放: ",target_span2.text,"移動排放: ",target_span3.text,"逸散排放: ",target_span4.text)
    print(sum(target_span1.text,target_span2.text,target_span3.text,target_span4.text))
  
def login_page(driver,user_id,user_pass):
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.ID, "login_username")))   #輸入帳號
        element.send_keys(user_id)

        element = wait.until(EC.visibility_of_element_located((By.ID, "login_password")))   #輸入密碼
        element.send_keys(user_pass)
        time.sleep(5)
        
        
        # silder = driver.find_element(By.CSS_SELECTOR,"div[class='ant-slider-handle']")
        # # background_image = driver.find_element(By.CSS_SELECTOR,"img[class='mb-2']")
        # # silder_image = driver.find_element(By.CSS_SELECTOR,"img[class='position-absolute start-0 top-0']")
        # action = ActionChains(driver)
        # action.click_and_hold(silder)
        # action.move_by_offset(200, 0).perform()
        # action.release().perform()
        # time.sleep(3)
    # element = wait.until(EC.visibility_of_element_located((By.ID, "login_verificationCode")))   #輸入驗證碼
    # element.send_keys("success")

        checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")  #勾選同意使用條款
        checkbox.click()
    
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))    #登入submit
        button.click()
    
    # time.sleep(3)

        autotest_td = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[text()='測試盤查']"))   #要測試的盤查計畫名稱 或是 編號(地球醫生=A廠區)
    )
    
    # 找到父 <tr> 元素
        parent_tr = autotest_td.find_element(By.XPATH, './parent::tr')
    
        button = parent_tr.find_element(By.XPATH, './/button[@type="button" and contains(@class, "ant-btn ant-btn-round ant-btn-link ant-btn-icon-only text-primary  border-0")]')
    #JavaScript寫法
        driver.execute_script("arguments[0].click()", button)
        time.sleep(1)

    
        link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "產業低碳化輔導計畫-溫室氣體盤查報告書")))   #點擊排放資料輸入
        link.click()
        time.sleep(5)


        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='第五章 基準年']")))
        element.click()
        
        time.sleep(2)
        calculate_co2_mobileCombustion(driver)
        
 
        
        

def main(): 

    logging.basicConfig(
        filename='autotest.log',  # 指定日誌輸出的檔案名稱
        level=logging.INFO,  # 設定日誌級別（這裡設定為 INFO 級別，可以自行調整）
        format='%(asctime)s - %(levelname)s - %(message)s',  # 設定日誌格式
        datefmt='%Y-%m-%d %H:%M:%S'  # 設定日期格式
    )

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('-headless')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--start-maximized") 
    service = Service(executable_path='C:\\Users\\iou85\\netzero-selenium\\chromedriver-win64\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    print("================================================================\n")
    print("請問要測試的網站是 ??? 1.prod 2.demo2 3.地球醫生 4.9999 5.8888 ")
    print("請輸入 : \n")
    site_num = int(input())
    # site_num =1
    site_dict={1:"https://220.132.206.5:8888",2:"https://192.168.0.132:9999/project",3:"https://prod.netzero.com.tw"}
    url=site_dict[site_num]
    
    driver.get(url)  
    if  site_num==3:      # 如果是iii or 9999登入帳密是 IIIII 跟 IIIIII
        user_id='user30000'
        user_pass='IIIComany!55665566'
    else:                               # 如果是公有雲 帳密都是 testCompany
        user_id='user08000'
        user_pass='IIIComany!55665566'
    login_page(driver,user_id,user_pass)   #自動登入至排放源輸入


main()