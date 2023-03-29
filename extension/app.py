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

def generate(text, model_path = r't5-model', tokenizer_path = r't5-model'):
  tokenizer = T5Tokenizer.from_pretrained(model_path, return_tensors = 'pt')
  model = T5ForConditionalGeneration.from_pretrained(tokenizer_path, return_dict = True)
  model.eval()
  input_ids = tokenizer.encode(text, return_tensors = 'pt')
  outputs = model.generate(input_ids)
  return tokenizer.decode(outputs[0]).strip('<pad>').strip('</s>').strip()

def load(text):
    ''' Takes in html page and load it's content and return objects as structured data.'''
    # structured_data = 'animals | action | filter && animals | location | center'
    # structured_data = 'Hotels | action | sort && Hotels | human_readable_position | top-left'.replace('_',' ').replace('-',' ')
    structured_data = text
    print(structured_data)
    return structured_data

# @app.route('/')
def speak(text = 'Hotels | action | sort && Hotels | human_readable_position | top-left'):
    '''converts text to speech'''
    print('text: ',text)
    text = text.replace('_',' ').replace('-',' ')
    print('text: ',text)
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

def classify(feature_df, filename=r'Model\search_model.sav'):
    classifier_model = pickle.load(open(filename,'rb'))
    coordinates = feature_df.pop('coordinates')
    feature_df['predictions'] = classifier_model.predict(feature_df.values)
    # print('predictions:\n',feature_df["predictions"],'\n\ncoordinates:\n',coordinates)
    print(feature_df.head())


@app.route('/trigger/')
def trigger(features = ['has_inner_text', 'has_search_inner_text', 'num_search', 'has_button', 'has_search_attr', 'coordinates']):
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
    # text = request.args['text']
    
    feature_dict = {feature: request.args.get(feature) for feature in features}
    print('feature_dict: ',feature_dict)
    print('len(feature_dict): ',len(feature_dict))
    for k in feature_dict.keys():
        print(k,':',len(feature_dict[k]),'\n', feature_dict[k])
        feature_dict[k] = feature_dict[k].split()
        if not feature_dict[k][0].isnumeric():
            feature_dict[k] = [list(map(float, row.split(','))) for row in feature_dict[k]]
        else:
            feature_dict[k] = list(map(float, feature_dict[k]))
    

        print(k,':',len(feature_dict[k]), feature_dict[k][0])
        
    feature_df = pd.DataFrame(feature_dict)
    print(feature_df.head())
    print('info:')
    print(feature_df.info())
    classify(feature_df)
    text = ''
    for text in ['Hotels | action | search && Hotels | human_readable_position | top', 'Hotels | action | sort && Hotels | human_readable_position | top-right', 'Hotels | action | filter && Hotels | human_readable_position | left', 'Results | action | discover && Results | location | center-bottom-right']:
        speak(generate(load(text)))
    return text


# if __name__ == '__main__':
    # app.run()
    # for text in load(''):
    #     print(text)
    # for text in ['Hotels | action | search && Hotels | human_readable_position | top', 'Hotels | action | sort && Hotels | human_readable_position | top-right','Hotels | action | filter && Hotels | human_readable_position | left', 'Results | action | discover && Results | location | bottom-right']:
    #     speak(generate(load(text)))
    # map(lambda text: speak(generate(text)), load(''))
    # trigger()

