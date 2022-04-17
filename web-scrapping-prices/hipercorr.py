
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

urllib3.disable_warnings()
t0 = time.time()

# CREATE THE DATAFRAME
scrap_list = pd.DataFrame(columns=['Producto', 'Precio'])

# Selenium browser
PATH = "C:/Users/Usuario/Google Drive/02_Business/Cursos/Keepcoding/KC_Proyecto_preliminarSara/scrapping/chromedriver_win32/chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service=s)

for i in list(range(1,17)):

    url = "https://www.hipercor.es/supermercado/frescos/frutas-y-verduras/verduras-y-hortalizas/"+str(i)+"/"
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)

    # # We make a slow scroll to the end of the page
    # total_height = 30000
    #
    # # Velocidad de scroll
    # for i in range(1, total_height, 10):
    #     driver.execute_script("window.scrollTo(0, {});".format(i))


    # we get the internal html code of the body
    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML')

    # CREATION OF BEAUTIFULSOUP OBJECT
    # url = 'https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059699-frutas/'
    # req = urllib3.PoolManager()
    # res = req.request('GET', url)
    soup = BeautifulSoup(source, 'html.parser')
    print(soup)

    # EXTRACTION OF ALL PRODUCTS NAMES IN THE SINGLE PAGE
    scrap_name = [i.text.strip() for i in soup.findAll('h3', {'class': 'text__Text-sc-1ddlex6-0 dhcXWY'})]
    product_name = pd.DataFrame(scrap_name, columns=['Producto'])

    # EXTRACTION OF ALL PRODUCTS PRICES IN THE SINGLE PAGE
    scrap_price = [i.text.strip() for i in soup.findAll('strong', {'class': 'base__Price-sc-1m8b7ry-30 fFUfak'})]
    product_price = pd.DataFrame(scrap_price, columns=['Precio'])

    # CONCATENATE THE RESULT ON THE DATAFRAME
    scrap_list = scrap_list.append(pd.concat([product_name['Producto'], product_price['Precio']],
                                             axis=1))
    print(i)

t1 = time.time()
r = t1 - t0
print(r)
print(scrap_list)

driver.close()
