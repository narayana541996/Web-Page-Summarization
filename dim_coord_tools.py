from selenium import webdriver
from selenium.webdriver.common.by import By


def find_viewport_dims_coords(chrome : webdriver):
    ''' Find dimensions and coordinates of viewport.'''
    viewport_width = chrome.execute_script('return window.innerWidth')
    # print('width: ',viewport_width)
    viewport_height = chrome.execute_script('return window.innerHeight')
    # print('height: ',viewport_height)
    viewport_center = {'x' : int(viewport_width / 2), 'y' : int(viewport_height / 2)}
    # print('center: ',viewport_center)
    # print('viewport_height: ', viewport_height,' viewport_width: ',viewport_width,' viewport_center: ',viewport_center)
    return {'viewport_height' : viewport_height, 'viewport_width' : viewport_width, 'viewport_center' : viewport_center}

def find_element_center_coords(element):
    element_center = {}
    element_center['y'] = (element.location['y'] + element.size['height']) / 2
    element_center['x'] = (element.location['x'] + element.size['width']) / 2
    print('element_center: ',element_center)
    return element_center

def find_element_region(element, viewport_dims_coords):
    ''' Find in which region of the viewport, an element is found'''
    region = {'left' : False,'right' : False, 'top' : False, 'bottom' : False, 
    'closer_to_center_x' : False, 'closer_to_center_y' : False, 'closer_to_right_end' : False, 'closer_to_left_end' : False,
    'closer_to_top' : False, 'closer_to_bottom' : False}
    element_center = find_element_center_coords(element)
    if element_center['x'] < viewport_dims_coords['viewport_center']['x']:
        region['left'] = True
    if element_center['x'] > viewport_dims_coords['viewport_center']['x']:
        region['right'] = True
    if element_center['y'] < viewport_dims_coords['viewport_center']['y']:
        region['top'] = True
    if element_center['y'] > viewport_dims_coords['viewport_center']['y']:
        region['bottom'] = True

    if abs(element_center['x'] - viewport_dims_coords['viewport_center']['x']) < (viewport_dims_coords['viewport_center']['x'] / 2):
        region['closer_to_center_x'] = True # if element is close to center horizontally.
    else:
        if (element_center['x'] - viewport_dims_coords['viewport_center']['x']) > 0:
            region['closer_to_right_end'] = True
        elif (element_center['x'] - viewport_dims_coords['viewport_center']['x']) < 0:
            region['closer_to_left_end'] = True
    
    if abs(element_center['y'] - viewport_dims_coords['viewport_center']['y']) < (viewport_dims_coords['viewport_center']['y'] / 2):
        region['closer_to_center_y'] = True # if element is close to center vertically.
    else:
        if (element_center['y'] - viewport_dims_coords['viewport_center']['y']) > 0:
            region['closer_to_bottom'] = True
        elif (element_center['y'] - viewport_dims_coords['viewport_center']['y']) < 0:
            region['closer_to_top'] = True
    return region

if __name__ == '__main__':
    url = r'https://www.expedia.com/Hotel-Search?&destination=Scotland%2C%20United%20KingdomregionId=11219&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2022-12-26&theme=&useRewards=false&userIntent='
    with webdriver.Chrome() as chrome:
        chrome.get(url)
        chrome.fullscreen_window()
        print('viewport_dims_coords: ',find_viewport_dims_coords(chrome))
        element = chrome.find_element(By.CSS_SELECTOR, 'form > input')
        print('element: ',element.id,'region: ', find_element_region(element, find_viewport_dims_coords(chrome)))