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

URL = "" 
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url=URL)

print("current url: ",driver.current_url)

wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, ''))).click()
# element = driver.find_element(By.CLASS_NAME,'nm-collections-row-gallery-li')
# driver.execute_script("arguments[0].click();", element)
