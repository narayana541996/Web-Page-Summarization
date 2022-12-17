#web and browser
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

def find_element_center_coords(element, viewport_dims_coords):
    ''' Find coordinates of the center of the visible part of the element. '''
    element_center = {}
    height = element.size['height']
    width = element.size['width']
    if element.location['y'] + element.size['height'] > (viewport_dims_coords['viewport_height'] - element.location['y']):
        height = abs(height - viewport_dims_coords['viewport_height'])
    if element.location['x'] + width > (viewport_dims_coords['viewport_width'] - element.location['x']):
        width = abs(width - viewport_dims_coords['viewport_width'])
    element_center['x'] = (element.location['x'] + width) / 2
    element_center['y'] = (element.location['y'] + height) / 2
    # print('element_center: ',element_center)
    return element_center

def find_element_region(element, viewport_dims_coords):
    ''' Find in which region of the viewport, an element is found '''
    region = {'left' : False,'right' : False, 'top' : False, 'bottom' : False} 
    reference_proximity = {'closer_to_center_x' : False, 'closer_to_center_y' : False, 'closer_to_right_end' : False, 'closer_to_left_end' : False,
    'closer_to_top' : False, 'closer_to_bottom' : False}
    element_center = find_element_center_coords(element, viewport_dims_coords)
    if element_center['x'] < viewport_dims_coords['viewport_center']['x']:
        region['left'] = True
    if element_center['x'] > viewport_dims_coords['viewport_center']['x']:
        region['right'] = True
    if element_center['y'] < viewport_dims_coords['viewport_center']['y']:
        region['top'] = True
    if element_center['y'] > viewport_dims_coords['viewport_center']['y']:
        region['bottom'] = True

    if abs(element_center['x'] - viewport_dims_coords['viewport_center']['x']) < (viewport_dims_coords['viewport_center']['x'] / 2):
        reference_proximity['closer_to_center_x'] = True # if element is close to center horizontally.
    else:
        if (element_center['x'] - viewport_dims_coords['viewport_center']['x']) > 0:
            reference_proximity['closer_to_right_end'] = True
        elif (element_center['x'] - viewport_dims_coords['viewport_center']['x']) < 0:
            reference_proximity['closer_to_left_end'] = True
    
    if abs(element_center['y'] - viewport_dims_coords['viewport_center']['y']) < (viewport_dims_coords['viewport_center']['y'] / 2):
        reference_proximity['closer_to_center_y'] = True # if element is close to center vertically.
    else:
        if (element_center['y'] - viewport_dims_coords['viewport_center']['y']) > 0:
            reference_proximity['closer_to_bottom'] = True
        elif (element_center['y'] - viewport_dims_coords['viewport_center']['y']) < 0:
            reference_proximity['closer_to_top'] = True
    return region, reference_proximity

def find_human_readable_position(element, chrome):
    '''returns position in human-friendly format.'''
    region, reference_proximity = find_element_region(element, find_viewport_dims_coords(chrome))
    position = ''
    if region['top']:
        position += '_top'
    elif region['bottom']:
        position += '_bottom'
    
    if region['right']:
        position += '_right'
    elif region['left']:
        position += '_left'
    
    close_reference = ''
    
    if reference_proximity['closer_to_top']:
        close_reference += '_top'
    elif reference_proximity['closer_to_bottom']:
        close_reference += '_bottom'

    if reference_proximity['closer_to_center_y']:
        if reference_proximity['closer_to_center_x']:
            close_reference += '_center'

    if reference_proximity['closer_to_left_end']:
        close_reference += '_left'
    elif reference_proximity['closer_to_right_end']:
        close_reference += '_right'
    return position.strip('_'), close_reference.strip('_')
        





if __name__ == '__main__':
    url = r'https://www.expedia.com/Hotel-Search?&destination=Scotland%2C%20United%20KingdomregionId=11219&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2022-12-26&theme=&useRewards=false&userIntent='
    with webdriver.Chrome() as chrome:
        chrome.get(url)
        chrome.fullscreen_window()
        print('viewport_dims_coords: ',find_viewport_dims_coords(chrome))
        element = chrome.find_element(By.CSS_SELECTOR, 'div.uitk-layout-grid-item')
        print('element: ',element.tag_name,'element.type',element.get_attribute('class'),'region: ', find_element_region(element, find_viewport_dims_coords(chrome)))
        print('human - pos: ',find_human_readable_position(element, chrome))


        '''
        TODO: 
        Instead of center, use vertical boundaries to specify vertical position, horizontal boundaries to specify horizontal position.
        Try to find position wrt cursor.
        '''