# auxiliary
import time
import sys
sys.path.insert(0, r'C:\assignments\cs733-nlp\web-page-summarizer')

# nlp
## custom modules
from text_generator import generate


# speech
from io import BytesIO
from gtts import gTTS
from pygame import mixer
from mutagen.mp3 import MP3

# web and browser
# from flask import Flask, jsonify, request
# from flask_cors import CORS
from pywinauto import Application


def load(html):
    ''' Takes in html page and load it's content and return objects as structured data.'''
    structured_data = 'animals | action | filter && animals | location | center'
    return structured_data

def speak(text):
    '''converts text to speech'''
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


# app = Flask(__name__)
# CORS(app)

def trigger():
    chrome = Application('uia')
    chrome.connect(title_re = ".*Chrome*", visible_only = True)
    item = 'Address and search bar'
    url = chrome.top_window().child_window(title = item, control_type = 'Edit').get_value()
    print(url)
    speak(generate(load(url)))


if __name__ == '__main__':
    trigger()