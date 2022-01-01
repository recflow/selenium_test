import selenium
import time
from movie_info import Movie
from mysql_save import DBMySql
from selenium import webdriver

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
sec = config.sections()
print("sec: ", sec)
URL = "https://www.netflix.com/browse"

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
    if nf_user.get_attribute('innerText')==config['netflix']['profile']:
        wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-name')))
        print(nf_user.get_attribute('innerText'))
        nf_user.click()
    break

wait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"ptrack-content")))

URL+="/genre/34399"
driver.get(url=URL)
print("current url: ",driver.current_url)

wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ptrack-content')))
contents = driver.find_elements(By.CLASS_NAME, 'slider-item')

def take_movie_info(content):
    time.sleep(2)
    wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ptrack-content')))
    ActionChains(driver).move_to_element(content).perform()
    wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'buttonControls--expand-button'))).click()

    # 가져올 정보
    # 1. 영화 제목
    title = driver.find_element(By.CLASS_NAME, 'about-header').find_element(By.TAG_NAME, 'strong').get_attribute('innerText')

    meta_data = driver.find_element(By.CLASS_NAME, 'videoMetadata--container')
    # 2. 영화 개봉연도
    year = meta_data.find_element(By.CLASS_NAME, 'year').get_attribute('innerText')
    # 3. 런닝 타임
    duration = meta_data.find_element(By.CLASS_NAME, 'duration').get_attribute('innerText')
    # 4. 관람 연령
    about = driver.find_element(By.CLASS_NAME, 'about-container')
    maturity = about.find_element(By.CLASS_NAME, 'maturityDescription').get_attribute('innerText')

    genres=''
    characteristic=''
    actors=''
    producer=''
    authors=''

    v_informs = about.find_elements(By.CLASS_NAME, 'previewModal--tags')
    for info in v_informs:
        column = info.find_elements(By.CLASS_NAME, 'previewModal--tags-label')
        for col in column:
            col_name = col.get_attribute('innerText')
            # 5. 장르
            if col_name == '장르:':
                genre = info.find_elements(By.TAG_NAME, 'a')
                for category in genre:
                    genres+=category.get_attribute('innerText')
            # 6. 특징
            elif col_name == '영화 특징:':
                characters = info.find_elements(By.TAG_NAME, 'a')
                for character in characters:
                    characteristic+=character.get_attribute('innerText')
            # 7. 출연자
            elif col_name == '출연:':
                acts =  info.find_elements(By.TAG_NAME, 'a')
                for act in acts:
                    actors += act.get_attribute('innerText')
            # 8. 감독
            elif col_name == '감독:':
                produces =  info.find_elements(By.TAG_NAME, 'a')
                for pd in produces:
                    producer+=pd.get_attribute('innerText')
            # 9. 각본
            elif col_name == '각본:':
                writers =  info.find_elements(By.TAG_NAME, 'a')
                for writer in writers:
                    authors+=writer.get_attribute('innerText')
    # 10. 줄거리
    synopsis = driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/p').get_attribute('innerText')
    # 11. 영화 이미지 주소
    wrapper=driver.find_element(By.CLASS_NAME, "videoMerchPlayer--boxart-wrapper")
    poster = wrapper.find_element(By.CLASS_NAME,"previewModal--boxart").get_attribute('src').split("?")[0]

    wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'previewModal-close'))).click()
    return Movie(title, synopsis, year, duration, maturity, genres, characteristic, actors, authors, producer, poster)

for i in range(len(contents)):
    # if i>=30:break
    movie_info = take_movie_info(contents[i])
    Movie.printMovieInfo(movie_info)
    DBMySql.connectMysql(movie_info)

LOGOUT="https://www.netflix.com/SignOut"
driver.get(url=LOGOUT)