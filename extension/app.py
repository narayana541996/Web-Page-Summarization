# auxiliary
import time
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

def generate(text, model_path = r't5-model', tokenizer_path = r't5-model'):
  tokenizer = T5Tokenizer.from_pretrained(model_path, return_tensors = 'pt')
  model = T5ForConditionalGeneration.from_pretrained(tokenizer_path, return_dict = True)
  model.eval()
  input_ids = tokenizer.encode(text, return_tensors = 'pt')
  outputs = model.generate(input_ids)
  return tokenizer.decode(outputs[0]).strip('<pad>').strip('</s>').strip()

def load(html):
    ''' Takes in html page and load it's content and return objects as structured data.'''
    # structured_data = 'animals | action | filter && animals | location | center'
    structured_data = 'Hotels | action | sort && Hotels | human_readable_position | top-left'.replace('_',' ').replace('-',' ')
    # structured_data = ['Hotels | action | search && Hotels | human_readable_position | top', 'Hotels | action | sort && Hotels | human_readable_position | top-right','Hotels | action | filter && Hotels | human_readable_position | left', 'Hotels | action | find search results && Hotels | location | bottom-right']
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


@app.route('/trigger')
def trigger():
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
    text = ''
    speak(generate(load(text)))
    return text


if __name__ == '__main__':
    # app.run()
    # for text in load(''):
    #     print(text)
    speak(generate(load('Hotels | action | filter && Hotels | human_readable_position | left')))
    # map(lambda text: speak(generate(text)), load(''))
