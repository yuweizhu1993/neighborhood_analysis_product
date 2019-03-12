##################################
#DFP project
#Part I: Get Data - Web Scrapping Using Selenium
#Data Source: RenFin
#Author: Yuwei Zhu

###################################
#import modules
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import re
import pandas as pd

#####################################
#helper function to click table button to get into table option
def table_option():
    driver.find_element_by_xpath('//*[@id="sidepane-header"]/div[2]/div/div[3]/button[2]').click()

#function to get all address
def get_address():
    address = []
    table = driver.find_elements_by_class_name('col_address')
    for i in table:
        address.append(i.text)
    return address

#function to get all location
def get_location():
    location = []
    table = driver.find_elements_by_class_name('col_location')
    for i in table:
        location.append(i.text)
    return location

#function to get all price
def get_price():
    price = []
    table = driver.find_elements_by_class_name('col_price')
    for i in table:
        price.append(i.text)
    return price

#function to get all number of beds
def get_beds():
    beds = []
    table = driver.find_elements_by_class_name('col_beds')
    for i in table:
        beds.append(i.text)
    return beds

#function to get all number of baths
def get_baths():
    baths = []
    table = driver.find_elements_by_class_name('col_baths')
    for i in table:
        baths.append(i.text)
    return baths


def one_page_data():
    #table_option()
    dict= {}
    #dict['Address'] = get_address()
    #dict['Location'] = get_location()
    address = get_address()
    location = get_location()
    price = get_price()
    beds = get_beds()
    baths = get_baths()
    dict[address[0]] = address[1:-1]
    dict[location[0]] = location[1:-1]
    dict[price[0]] = price[1:-1]#have to drop the last row, which is average
    dict[beds[0]] = beds[1:-1]
    dict[baths[0]] = baths[1:-1]
    df = pd.DataFrame(dict)
    return df

#function loop through pages to get data
def loop_pages(empty_df,number):
    page = 0
    while page < number:
        df = one_page_data()
        empty_df = empty_df.append(df)
        driver.find_element_by_xpath('//*[@id="right-container"]/div[3]/div/div[3]/button[2]').click()
        page += 1
        time.sleep(2)
    return empty_df


#first create an empty data frame
header = ['Address', 'Location', 'Price','Beds','Baths']
empty_dict = {}
for i in header:
    empty_dict[i] = []

empty_df = pd.DataFrame(empty_dict)

driver = webdriver.Chrome()
driver.implicitly_wait(30)
url = "https://www.redfin.com/city/15702/PA/Pittsburgh"
driver.get(url)
table_option()

df = loop_pages(empty_df,15)

#wirte csv file
df.to_csv('data_houseprice.csv')