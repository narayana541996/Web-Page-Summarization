from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from collections import defaultdict
from time import sleep
import pandas as pd
import numpy as np

def return_element_values(object, chrome, columns): #returns a list of the values of features
    element_values = {}
    all_element_values = []
    for element in chrome.find_elements(By.TAG_NAME, object):
        for col in columns:
            try:
                WebDriverWait(chrome,5).until(EC.presence_of_element_located((By.ID, element.id)))
                element_values[col] = element.get_attribute(col)
                
            except (TimeoutException, StaleElementReferenceException, NoSuchElementException):
                element_values[col] = None
                continue
        all_element_values.append(list(element_values.values()))
    return all_element_values

            
    # return [[element.tag_name, element.get_attribute('name'), element.get_dom_attribute('class'), element.get_dom_attribute('id'), element.text, element.location, element.size, chrome.find_element(By.CLASS_NAME, element.get_dom_attribute("class"))] for element in chrome.find_elements(By.TAG_NAME, object)]

def make_dataset(url, columns = ['tag', 'name', 'class','id', 'text']): #Creates dataset using return_element_values(object, chrome)
    with webdriver.Chrome() as chrome:
        chrome.maximize_window()
        chrome.get(url) #opens a url in chrome
        WebDriverWait(chrome,5).until(EC.presence_of_all_elements_located((By.TAG_NAME,'*')))
        object_values = []
        for object in ['button','form','field','input']:
            # try:
            object_values.append(pd.DataFrame(return_element_values(object, chrome, columns), columns= columns))
            # except (StaleElementReferenceException, NoSuchElementException) as e:
            #     continue
        return pd.concat(object_values)
        # return pd.concat(map(lambda object: pd.DataFrame(return_element_values(object, chrome), columns= columns), ['button','form','field']))

###########driver code
web_data = pd.DataFrame(columns = ['tag', 'name', 'class','id', 'text','location','size', 'first_class_element'])
for url in [r"https://www.reddit.com/r/learnprogramming/top/?t=month",r'https://www.mercadolivre.com.br/#from=homecom',r'https://www.indeed.com/',r'https://www.tripadvisor.com/',r'https://www.yellowpages.com/']:
    web_data = pd.concat( [web_data, make_dataset(url, web_data.columns)])
print(web_data.info())
print(web_data)