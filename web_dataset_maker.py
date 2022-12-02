# -*- coding: utf-8 -*-
"""web_dataset_maker.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14XQoFcWwCfXCjPoTIC1g-ilA_3o59o4r
"""

# !pip install selenium

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, NoSuchAttributeException
from collections import defaultdict
from time import sleep
import pandas as pd
import numpy as np

def return_element_values(object, chrome): #returns a list of the values of features
    element_values = {}
    all_element_values = []
    for element in chrome.find_elements(By.TAG_NAME, object):
        element_values['tag'] = element.tag_name
        element_values['size'] = element.size
        element_values['location'] = element.location
        element_values['text'] = element.text
        
        for col in ['id','name','class']:
            try:
                # WebDriverWait(chrome).until(EC.presence_of_element_located((By.ID, element.id)))
                attribute = element.get_attribute(col)
                if attribute and attribute.strip():
                    element_values[col] = attribute
                
            except (TimeoutException, StaleElementReferenceException, NoSuchElementException):
                element_values[col] = np.nan
        try:
            element_values['first_class_div'] = chrome.find_element(By.CLASS_NAME, element_values["class"]).id
        except NoSuchAttributeException:
            try:
                element_values['first_class_div'] = chrome.find_element(By.CLASS_NAME, element_values["class"]).get_attribute('name')
            except:
                element_values['first_class_div'] = np.nan
        except (TimeoutException, StaleElementReferenceException, NoSuchElementException, KeyError):
            element_values['first_class_div'] = np.nan
                
        all_element_values.append(element_values)
    return all_element_values

def make_dataset(url, columns = ['tag', 'name', 'class','id', 'text']): #Creates dataset using return_element_values(object, chrome)
    with webdriver.Chrome() as chrome:
        chrome.maximize_window()
        chrome.get(url) #opens a url in chrome
        WebDriverWait(chrome,5).until(EC.presence_of_all_elements_located((By.TAG_NAME,'*')))
        object_values = []
        for object in ['button','form','field','input', 'nav']:
            # try:
            object_values.append(pd.DataFrame(return_element_values(object, chrome), columns= columns).fillna(np.nan))
            # except (StaleElementReferenceException, NoSuchElementException) as e:
            #     continue
        return pd.concat(object_values)
        # return pd.concat(map(lambda object: pd.DataFrame(return_element_values(object, chrome), columns= columns), ['button','form','field']))

###########driver code
web_data = pd.DataFrame(columns = ['tag', 'name', 'class','id', 'text','location','size', 'first_class_div'])
for url in [r"https://www.reddit.com/r/learnprogramming/top/?t=month",r'https://www.mercadolivre.com.br/#from=homecom',r'https://www.indeed.com/',r'https://www.tripadvisor.com/',r'https://www.yellowpages.com/',r'https://www.ebay.com/',r'https://www.ebay.com/b/PC-Gaming/bn_7000259657']:
    web_data = pd.concat( [web_data, make_dataset(url, web_data.columns)])
print(web_data.info())
web_data