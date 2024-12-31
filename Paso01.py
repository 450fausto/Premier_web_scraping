import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pathlib as pl
import csv

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

driver.get('https://www.skysports.com/premier-league-results/2023-24')

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

boton = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.XPATH, '//button[@class="plus-more"]'))
     )
    
boton.click()
sleep(random.uniform(9,12))

links_crudo = driver.find_elements(By.XPATH, '//div[@class="fixres__body"]/div[@class="fixres__item"]//a[@class="matches__item matches__link"]')
links = []
for link in links_crudo:
    links.append(link.get_attribute('href'))

home = pl.Path('C:/Users/Usuario/Documents/Web_Scraping_Udemy/Premier_League')
name = 'links_premier.py'

doc = home / name

if not doc.exists():
    doc.touch()

# with doc.open(mode='w') as new:
    
#     writer = csv.writer(new, lineterminator='\n')

#     for i in links:
#         writer.writerow([i])

# Guardar la lista en un archivo Python (script)
with doc.open(mode = 'w') as archivo_script:
    archivo_script.write('partidos = ' + str(links))

