from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

urllib3.disable_warnings()

def eroski_frutas():

    t0 = time.time()

    # CREATE THE DATAFRAME
    scrap_list = pd.DataFrame(columns=['Producto', 'Precio'])

    # Selenium browser
    PATH = "C:/Users/Usuario/Google Drive/02_Business/Cursos/Keepcoding/KC_Proyecto_preliminarSara/scrapping/chromedriver_win32/chromedriver.exe"
    s = Service(PATH)
    driver = webdriver.Chrome(service=s)
    driver.get("https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059699-frutas/")
    driver.maximize_window()
    time.sleep(1)

    # We make a slow scroll to the end of the page
    total_height = 30000
    for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))

    # we get the internal html code of the body
    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML')

    # CREATION OF BEAUTIFULSOUP OBJECT
    soup = BeautifulSoup(source, 'html.parser')

    # EXTRACTION OF ALL PRODUCTS NAMES IN THE SINGLE PAGE
    scrap_name = [i.text.strip() for i in soup.findAll('h2', {'class': 'product-title product-title-resp'})]
    product_name = pd.DataFrame(scrap_name, columns=['Producto'])

    # EXTRACTION OF ALL PRODUCTS PRICES IN THE SINGLE PAGE
    scrap_price = [i.text.strip() for i in soup.findAll('span', {'class': 'price-offer-now'})]
    product_price = pd.DataFrame(scrap_price, columns=['Precio'])

    # CONCATENATE THE RESULT ON THE DATAFRAME
    scrap_list = scrap_list.append(pd.concat([product_name['Producto'], product_price['Precio']],
                                             axis=1))
    scrap_list.reset_index(drop=True)
    t1 = time.time()
    r = t1 - t0
    print(r)

    driver.close()

    return scrap_list


def eroski_verduras():

    t0 = time.time()

    # CREATE THE DATAFRAME
    scrap_list = pd.DataFrame(columns=['Producto', 'Precio'])

    # Selenium browser
    PATH = "C:/Users/Usuario/Google Drive/02_Business/Cursos/Keepcoding/KC_Proyecto_preliminarSara/scrapping/chromedriver_win32/chromedriver.exe"
    s = Service(PATH)
    driver = webdriver.Chrome(service=s)
    driver.get("https://supermercado.eroski.es/es/supermercado/2059698-frescos/2059710-verduras-y-hortalizas")
    driver.maximize_window()
    time.sleep(1)

    # We make a slow scroll to the end of the page
    total_height = 30000
    for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))

    # we get the internal html code of the body
    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML')

    # CREATION OF BEAUTIFULSOUP OBJECT
    soup = BeautifulSoup(source, 'html.parser')

    # EXTRACTION OF ALL PRODUCTS NAMES IN THE SINGLE PAGE
    scrap_name = [i.text.strip() for i in soup.findAll('h2', {'class': 'product-title product-title-resp'})]
    product_name = pd.DataFrame(scrap_name, columns=['Producto'])

    # EXTRACTION OF ALL PRODUCTS PRICES IN THE SINGLE PAGE
    scrap_price = [i.text.strip() for i in soup.findAll('span', {'class': 'price-offer-now'})]
    product_price = pd.DataFrame(scrap_price, columns=['Precio'])

    # CONCATENATE THE RESULT ON THE DATAFRAME
    scrap_list = scrap_list.append(pd.concat([product_name['Producto'], product_price['Precio']],
                                             axis=1))

    scrap_list.reset_index(drop=True)
    t1 = time.time()
    r = t1 - t0
    print(r)

    driver.close()

    return scrap_list
