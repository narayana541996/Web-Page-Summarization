# auxiliary
from logging import FileHandler, WARNING
import numpy as np ##### Add numpy, pandas, scikit-learn to requirements.txt
import pandas as pd
# import sklearn
import time
import pickle
import sys
sys.path.insert(0, r'C:\assignments\cs733-nlp\web-page-summarizer')

# nlp
## custom modules
# from extension.text_generator import generate
from transformers import T5Tokenizer, T5ForConditionalGeneration


# speech
from io import BytesIO
from gtts import gTTS
from pygame import mixer
from mutagen.mp3 import MP3

# web and browser
from flask import Flask, jsonify, request
from flask_cors import CORS
from selenium import webdriver
from pywinauto import Application

app = Flask(__name__)
CORS(app)
file_handler = FileHandler('log.txt')
file_handler.setLevel(WARNING)

def output_summary(text, model_path = r't5-model', tokenizer_path = r't5-model'):
  tokenizer = T5Tokenizer.from_pretrained(model_path, return_tensors = 'pt')
  model = T5ForConditionalGeneration.from_pretrained(tokenizer_path, return_dict = True)
  model.eval()
  input_ids = tokenizer.encode(text, return_tensors = 'pt')
  outputs = model.generate(input_ids)
  return tokenizer.decode(outputs[0]).strip('<pad>').strip('</s>').strip()

def generate_structured_summary(human_readable_position, element = 'search'):
    ''' Creates a structured data from human_readable_position, to be given as input to the summarizer in output_summary(). '''
    # print('hrpos: ',human_readable_position)
    # print('hrpos replaced _: ',human_readable_position[0].replace('_',' ').replace('-',' '))
    return f"{element} | location | {human_readable_position[0].replace('_',' ').replace('-',' ')} && {element} | near  | {human_readable_position[1].replace('_',' ').replace('-',' ')}"

def add_structured_summary(feature_df, element):
    ''' Takes dataframe with features and returns the dataframe with structured summary in a new column.'''
    # for col in ['action','human_readable_position']:
    #         element_values['model_input'] += f'{element_values["subject"]} | {col} | {element_values[col]} &&'
    #     element_values['model_input'] = element_values['model_input'].strip('&&').strip()
    # structured_data = 'animals | action | filter && animals | location | center'
    # structured_data = 'Hotels | action | sort && Hotels | human_readable_position | top-left'.replace('_',' ').replace('-',' ')
    feature_df['structured_summary_item'] = feature_df['human_readable_position'].map(lambda hrpos: generate_structured_summary(hrpos, element))
    # print(feature_df)
    return feature_df

# @app.route('/')
def speak(text = 'Hotels | action | sort && Hotels | human_readable_position | top-left'):
    '''converts text to speech'''
    # print('text: ',text)
    text = text.replace('_',' ').replace('-',' ')
    # print('text: ',text)
    mp3_file_object = BytesIO()
    tts = gTTS(text, lang='en')
    tts.write_to_fp(mp3_file_object)
    # mp3_file_object.seek(0)
    audio = MP3(mp3_file_object)
    mixer.init()
    mixer.music.load(mp3_file_object,'mp3')
    # mixer.music.rewind()
    mixer.music.play()
    print('freeze...')
    time.sleep(audio.info.length)
    return text

def classify(feature_df, filename):
    classifier_model = pickle.load(open(filename,'rb'))
    # coordinates = feature_df.pop('coordinates')
    print('feature_df["predictions"].cols: ',feature_df.head())
    feature_df['predictions'] = classifier_model.predict(feature_df[feature_df.columns[:-1]].values)
    # print('predictions:\n',feature_df["predictions"],'\n\ncoordinates:\n',coordinates)
    print(feature_df)
    feature_df = feature_df[feature_df['predictions'] == 1]
    return feature_df

def find_element_center(element_coords):
    return {'x' : int(element_coords[0]+abs(element_coords[0] - element_coords[2]) / 2), 'y' : int(element_coords[1] + abs(element_coords[1] - element_coords[3]) / 2)}
    
def find_element_region(element_coords, page_size):
    ''' Find in which region of the webpage, an element is found '''
    region = {'left' : False,'right' : False, 'top' : False, 'bottom' : False} 
    reference_proximity = {'closer_to_center_x' : False, 'closer_to_center_y' : False, 'closer_to_right_end' : False, 'closer_to_left_end' : False,
    'closer_to_top' : False, 'closer_to_bottom' : False}
    # print('element_coords: ',element_coords)
    element_center = find_element_center(element_coords)
    page_center = {'x' : int(page_size[0] / 2), 'y' : int(page_size[1] / 2)}
    if element_center['x'] < page_center['x']:
        region['left'] = True
    if element_center['x'] > page_center['x']:
        region['right'] = True
    if element_center['y'] < page_center['y']:
        region['top'] = True
    if element_center['y'] > page_center['y']:
        region['bottom'] = True

    if abs(element_center['x'] - page_center['x']) < (page_center['x'] / 2):
        reference_proximity['closer_to_center_x'] = True # if element is close to center horizontally.
    else:
        if (element_center['x'] - page_center['x']) > 0:
            reference_proximity['closer_to_right_end'] = True
        elif (element_center['x'] - page_center['x']) < 0:
            reference_proximity['closer_to_left_end'] = True
    
    if abs(element_center['y'] - page_center['y']) < (page_center['y'] / 2):
        reference_proximity['closer_to_center_y'] = True # if element is close to center vertically.
    else:
        if (element_center['y'] - page_center['y']) > 0:
            reference_proximity['closer_to_bottom'] = True
        elif (element_center['y'] - page_center['y']) < 0:
            reference_proximity['closer_to_top'] = True
    # print('inner region: ',region)
    # print('inner prox: ',reference_proximity)
    return (region, reference_proximity)

def find_human_readable_position(element_coords, page_size):
    '''returns position in human-friendly format.'''
    region, reference_proximity = find_element_region(element_coords, page_size)
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
        
    if close_reference.strip('_') != 'center':
        if len(close_reference.strip('_').split('_')) == 1:
            close_reference += '_end'
        elif len(close_reference.strip('_').split('_')) == 2:
            close_reference += '_corner'
    return position.strip('_'), close_reference.strip('_')


@app.route('/generate_summary/', methods = ['POST'])
def generate_summary():
    # driver = webdriver.Chrome()
    # url = driver.command_executor._url
    # print(url)
    # session_id = driver.session_id
    # driver = webdriver.Remote(url, desired_capabilities={})
    # driver.close()
    # driver.session_id = session_id
    # driver.get(url)
    # data = request.get_json()
    # data = jsonify(data)
    # chrome = Application('uia')
    # chrome.connect(title_re = ".*Chrome*", visible_only = True)
    # item = 'Address and search bar'
    # url = chrome.top_window().child_window(title = item, control_type = 'Edit').get_value()
    # print(url)
    # text = request.form['text']
    # print('request.form: ',len(request.form))
    # print('request.files: ',len(request.files))
    # print('request.values: ',len(request.values))
    # print('request.json: ',len(request.json))
    # print('request.get_json: ',len(request.get_json(force=True)))
    feature_json_dict = request.json
    print('json dict:\n',feature_json_dict)
    feature_df_dict = {} # {k : pd.DataFrame(feature_dict[k]) for k in feature_dict.keys()}
    dim_coord_dict = {}
    print('page_dims: ',feature_json_dict['page_width'],' ',feature_json_dict['page_height'])
    for k in feature_json_dict.keys():
        print('k:',k)
        if isinstance(feature_json_dict[k], dict):
            print(feature_json_dict[k])
            feature_df_dict[k] = pd.DataFrame(feature_json_dict[k]['features'])
            feature_df_dict[k]['coordinates'] = feature_df_dict[k]['coordinates'].map(tuple)
            feature_df_dict[k].drop_duplicates(keep='first')
            print('info:\n',feature_df_dict[k].info())
            print('head:\n',feature_df_dict[k].head())
        else:
            dim_coord_dict[k] = feature_json_dict[k]
    #         print('dim-coord-dict: ',dim_coord_dict)
    # print('feature_df keys: ',list(feature_df_dict.keys()))
    # print('dim_coord keys: ',list(dim_coord_dict.keys()))
    def speak_webpage_overview(feature_df_dict):
        '''Give an overview of the webpage mentioing all the selected elements present.'''
        element_count_dict = {element: len(feature_df_dict[element]) for element in feature_df_dict.keys()}
        elements_found = [element for element, count in element_count_dict.items() if count > 0]
        if len(elements_found) > 1:
            speak(output_summary('web page | overview | '+",".join(elements_found[:-1])+' and '+elements_found[-1] ))
        elif len(elements_found) == 1:
            speak(output_summary('web page | overview | '+elements_found[0]))

    filenames = {'search' : r'classifier-models\search_model.sav', 'filter' : r'classifier-models\filter_model_2.sav', 'sort' : r'classifier-models\sort_model_2.sav', 'page' : r'classifier-models\page_model_2.sav'}
    for element, feature_df in feature_df_dict.items():
        print('-----',element,':')
        feature_df.drop_duplicates(keep='first')
        print('feature_df.info:\n',feature_df.info())
        if len(feature_df) == 0:
            continue
        feature_df_dict[element] = classify(feature_df, filenames[element])
        # feature_df[['region']]
    speak_webpage_overview(feature_df_dict)
        
    for element, feature_df in feature_df_dict.items():
        region = feature_df['coordinates'].map(lambda c: find_element_region(c, [dim_coord_dict[k] for k in ['page_width', 'page_height']]))
        print('region: ',region)
        feature_df['region'], feature_df['reference_proximity'] = region.str[0], region.str[1]
        
        feature_df['human_readable_position'] = feature_df['coordinates'].map(lambda row: find_human_readable_position(row, [dim_coord_dict[k] for k in ['page_width', 'page_height']]))
        # print('reference_proximity')
        
        print(feature_df.head())
        feature_df = add_structured_summary(feature_df, element)
        feature_df['generated'] = feature_df['structured_summary_item'].map(output_summary)
        feature_df['generated'].map(speak)
        text = 'generate_summary() called.'
    return text


# if __name__ == '__main__':
    # app.run()
    # for text in load(''):
    #     print(text)
    # for text in ['Hotels | action | search && Hotels | human_readable_position | top', 'Hotels | action | sort && Hotels | human_readable_position | top-right','Hotels | action | filter && Hotels | human_readable_position | left', 'Results | action | discover && Results | location | bottom-right']:
    #     speak(generate(load(text)))
    # map(lambda text: speak(generate(text)), load(''))
    # trigger()

