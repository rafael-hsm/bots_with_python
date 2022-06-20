import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

research = input("Enter the search: ")
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.google.com")

find_research = driver.find_element(By.NAME, "q")
find_research.clear()
find_research.send_keys(research)
find_research.send_keys(Keys.ENTER)
time.sleep(1)
results = driver.find_element(By.XPATH, '//*[(@id = "result-stats")]')
print(results.text)

driver.close()
