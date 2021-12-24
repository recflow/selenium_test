import time
import selenium
from selenium import webdriver

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as wait

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8') 
sec = config.sections()
print("sec: ", sec)
URL = "https://www.netflix.com/browse/"

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url=URL)

driver.find_element(By.ID, 'id_userLoginId').send_keys(config['netflix']['id'])
driver.find_element(By.ID, 'id_password').send_keys(config['netflix']['pw'])
wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-button'))).click()

print("current url: ",driver.current_url)
wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'profile-name')))
nf_users=driver.find_elements(By.CLASS_NAME, 'profile-name')

for nf_user in nf_users:
    wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-name')))
    # time.sleep(2)    
    if nf_user.get_attribute('innerText')==config['netflix']['profile']:
        # time.sleep(2)
        wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-name')))    
        print(nf_user.get_attribute('innerText'))
        nf_user.click()
    break

wait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"ptrack-content")))

URL += "genre/34399"
driver.get(url=URL)
print("current url: ",driver.current_url)

wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ptrack-content')))
content = driver.find_elements(By.CLASS_NAME, 'ptrack-content')
for i in range(10):
    ActionChains(driver).move_to_element(driver.find_elements((By.CLASS_NAME, 'ptrack-content'))).perform()
    wait(driver, 10).until(EC.element_to_be_clickable(By.CLASS_NAME, 'previewModal--metadatAndControls-info')).click()

# # 가져올 정보
# # 1. 영화 제목
# title = driver.find_element(By.CLASS_NAME, 'about-header').find_element(By.TAG_NAME, 'strong').get_attribute('innerText')

# meta_data = driver.find_element(By.CLASS_NAME, 'videoMetadata--container')
# # 2. 영화 개봉연도
# year = meta_data.find_element(By.CLASS_NAME, 'year').get_attribute('innerText')
# # 3. 런닝 타임
# duration = meta_data.find_element(By.CLASS_NAME, 'duration').get_attribute('innerText')
# # 4. 관람 연령
# about = driver.find_element(By.CLASS_NAME, 'about-container')
# maturity = about.find_element(By.CLASS_NAME, 'maturityDescription')

# v_informs = about.find_elements(By.CLASS_NAME, 'previewModal--tags')
# for info in v_informs:
#     column = info.find_elements(By.CLASS_NAME, 'previewModal--tags-label').get_attribute('innerText')
#     for col in column:
#     # 5. 장르
#         if col == '장르':
#             genre = info.find_elements(By.TAG_NAME, 'a').get_attribute('innerText')
#     # 6. 특징

#     # 7. 출연자
#     # 8. 감독
# # 9. 줄거리
# synopsis = driver.find_element(By.CLASS_NAME, 'preview-modal-synopsis').get_attribute('innerText')

# print("제목: ", title)
# print("개봉연도", year)
# print("런닝 타임", duration)
# print("관람 연령", maturity)
# print("장르", genre)