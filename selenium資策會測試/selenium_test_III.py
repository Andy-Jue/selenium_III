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
import os

def login_page(driver,user_id,user_pass):
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.ID, "login_username")))   #輸入帳號
        element.send_keys(user_id)

        element = wait.until(EC.visibility_of_element_located((By.ID, "login_password")))   #輸入密碼
        element.send_keys(user_pass)
        time.sleep(5)

        checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")  #勾選同意使用條款
        checkbox.click()
    
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))    #登入submit
        button.click()
    
    # time.sleep(3)

        autotest_td = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[text()='user20000底下的user30000測試']"))   #要測試的盤查計畫名稱 或是 編號(地球醫生=A廠區)
    )
    
    # 找到父 <tr> 元素
        parent_tr = autotest_td.find_element(By.XPATH, './parent::tr')
    
        button = parent_tr.find_element(By.XPATH, './/button[@type="button" and contains(@class, "ant-btn ant-btn-round ant-btn-link ant-btn-icon-only text-primary  border-0")]')
    #JavaScript寫法
        driver.execute_script("arguments[0].click()", button)
        time.sleep(1)

    
        link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "排放資料輸入")))   #點擊排放資料輸入
        link.click()

def main(): 
    log_file_path = 'autotest.log'
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    logging.basicConfig(
        filename='autotest.log',  # 指定日誌輸出的檔案名稱
        level=logging.INFO,  # 設定日誌級別（這裡設定為 INFO 級別，可以自行調整）
        format='%(asctime)s - %(levelname)s - %(message)s',  # 設定日誌格式
        datefmt='%Y-%m-%d %H:%M:%S'  # 設定日期格式
    )

    current_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(current_dir, 'chromedriver-win64', 'chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    #options.add_argument('-headless')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--start-maximized")
    options.add_argument('--disable-web-security')
    options.add_argument('--ignore-certificate-errors')
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    print("================================================================\n")
    print("請問要測試的網站是 ??? 1.prod 2.demo2 3.中衛中心 4.8888 5.9999 ")
    print("請輸入 : \n")
    site_num = int(input())
    # site_num =1
    site_dict={1:"https://prod.netzero.com.tw/project",2:"https://demo2.netzero.com.tw/project",3:"https://csd.netzero.com.tw/project",4:"https://220.132.206.5:8888/project",5:"https://220.132.206.5:9999/project"}
    url=site_dict[site_num]
    
    driver.get(url)  
    if  site_num==1:      # 如果是iii or 9999登入帳密是 IIIII 跟 IIIIII
        user_id='user30000'
        user_pass='IIIComany!55665566'
    elif site_num == 3:
        user_id ='user_65c008'
        user_pass = 'IIIComany!55665566'
    else :
        user_id = 'user30000'
        user_pass = 'IIIComany!55665566'
    login_page(driver,user_id,user_pass)   #自動登入至排放源輸入
    print("請問要自動測試何種功能? 1:新增 2:匯入舊有模版 3:匯入資策會模版 4:編輯 5:刪除 6:excel匯出 7:新增多個 8:計算總值" )
    func = int(input())
    # func=1
    if func == 1:
        print("新增 自動測試")
        logging.info('================新增 開始================')
        source_input(driver,url)        #排放源輸入(有"新增"的)

        logging.info('================新增 結束================')

    elif func == 2:
        logging.info('================excel匯入 開始================')
        print("excel 自動匯入(舊有模版)")
        excel_input_old(driver,url,site_num)
        logging.info('================excel匯入 結束================')
    
    elif func == 3:
        logging.info('================excel匯入 開始================')
        print("excel 自動匯入(資策會模版)")
        excel_input_new(driver,url,site_num)
        logging.info('================excel匯入 結束================')

    elif func == 4:
        logging.info('================編輯 開始================')
        print("編輯 自動化測試")
        edit(driver,url)
        
        logging.info('================編輯 結束================')

    elif func == 5:
        logging.info('================刪除 開始================')
        print("刪除 自動化測試")
        delete(driver,url)
        logging.info('================刪除 結束================')

    elif func == 6 :
        logging.info('================excel匯出 開始================')
        temp_func = 'output'
        print("excel 自動匯出")
        excel_output(driver,url,temp_func)
        logging.info('================excel匯出 結束================')
    elif func == 7:
        logging.info('================新增多個 開始================')
        print("新增多個 自動測試")
        source_input_1(driver,url)       
        logging.info('================新增多個 結束================')
    elif func == 8:
        logging.info('================計算 開始================')
        print("計算總值")
        value_test(driver,url)
        
        logging.info('================計算 結束================')
    elif func == 9:
        logging.info('================計算 開始================')
        print("計算總值")
        value_test_2(driver,url)
        
        logging.info('================計算 結束================')
    # elif func == 7 :
    #     # logging.info('================excel模板下載 開始================')
    #     temp_func = 'download'
    #     print("excel 自動模板下載")
    #     excel_output(driver,url,temp_func)
    #     # logging.info('================excel模板下載 結束================')

main()