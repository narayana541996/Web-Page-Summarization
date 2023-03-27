# auxiliary
from logging import FileHandler, WARNING
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

def coroutine_primer(coroutine):
    def wrap(*args, **kwargs):
        cr = coroutine(*args, **kwargs)
        cr.next()
        return cr
    return wrap

@app.route('/trigger/')
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
    
    
    features = ['has_inner_text', 'has_search_inner_text', 'num_search', 'has_button', 'has_search_attr', 'coordinates']
    feature_dict = {feature: request.args.get(feature) for feature in features}
    print('len(features): ',len(features))
    for k in features.keys():
        print(k,':',len(features[k]))
        print(features[k])
    ############# Use coroutine/generator to convert the parameters into features
    text = ''
    for text in ['Hotels | action | search && Hotels | human_readable_position | top', 'Hotels | action | sort && Hotels | human_readable_position | top-right','Hotels | action | filter && Hotels | human_readable_position | left', 'Results | action | discover && Results | location | center-bottom-right']:
        speak(generate(load(text)))
    return text


if __name__ == '__main__':
    # app.run()
    # for text in load(''):
    #     print(text)
    # for text in ['Hotels | action | search && Hotels | human_readable_position | top', 'Hotels | action | sort && Hotels | human_readable_position | top-right','Hotels | action | filter && Hotels | human_readable_position | left', 'Results | action | discover && Results | location | bottom-right']:
    #     speak(generate(load(text)))
    # map(lambda text: speak(generate(text)), load(''))
    trigger()


'''
Looking in indexes: https://pypi.org/simple, https://us-python.pkg.dev/colab-wheels/public/simple/
Collecting transformers
  Downloading transformers-4.25.1-py3-none-any.whl (5.8 MB)
     |████████████████████████████████| 5.8 MB 21.8 MB/s 
Requirement already satisfied: tqdm>=4.27 in /usr/local/lib/python3.8/dist-packages (from transformers) (4.64.1)
Requirement already satisfied: packaging>=20.0 in /usr/local/lib/python3.8/dist-packages (from transformers) (21.3)
Requirement already satisfied: requests in /usr/local/lib/python3.8/dist-packages (from transformers) (2.23.0)
Requirement already satisfied: pyyaml>=5.1 in /usr/local/lib/python3.8/dist-packages (from transformers) (6.0)
Requirement already satisfied: regex!=2019.12.17 in /usr/local/lib/python3.8/dist-packages (from transformers) (2022.6.2)
Collecting tokenizers!=0.11.3,<0.14,>=0.11.1
  Downloading tokenizers-0.13.2-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (7.6 MB)
     |████████████████████████████████| 7.6 MB 66.0 MB/s 
Requirement already satisfied: numpy>=1.17 in /usr/local/lib/python3.8/dist-packages (from transformers) (1.21.6)
Collecting huggingface-hub<1.0,>=0.10.0
  Downloading huggingface_hub-0.11.1-py3-none-any.whl (182 kB)
     |████████████████████████████████| 182 kB 75.3 MB/s 
Requirement already satisfied: filelock in /usr/local/lib/python3.8/dist-packages (from transformers) (3.8.0)
Requirement already satisfied: typing-extensions>=3.7.4.3 in /usr/local/lib/python3.8/dist-packages (from huggingface-hub<1.0,>=0.10.0->transformers) (4.4.0)
Requirement already satisfied: pyparsing!=3.0.5,>=2.0.2 in /usr/local/lib/python3.8/dist-packages (from packaging>=20.0->transformers) (3.0.9)
Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in /usr/local/lib/python3.8/dist-packages (from requests->transformers) (1.24.3)
Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.8/dist-packages (from requests->transformers) (2022.9.24)
Requirement already satisfied: idna<3,>=2.5 in /usr/local/lib/python3.8/dist-packages (from requests->transformers) (2.10)
Requirement already satisfied: chardet<4,>=3.0.2 in /usr/local/lib/python3.8/dist-packages (from requests->transformers) (3.0.4)
Installing collected packages: tokenizers, huggingface-hub, transformers
Successfully installed huggingface-hub-0.11.1 tokenizers-0.13.2 transformers-4.25.1
Looking in indexes: https://pypi.org/simple, https://us-python.pkg.dev/colab-wheels/public/simple/
Collecting sentencepiece
  Downloading sentencepiece-0.1.97-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.3 MB)
     |████████████████████████████████| 1.3 MB 15.7 MB/s 
Installing collected packages: sentencepiece
Successfully installed sentencepiece-0.1.97
Looking in indexes: https://pypi.org/simple, https://us-python.pkg.dev/colab-wheels/public/simple/
Collecting pytorch
  Downloading pytorch-1.0.2.tar.gz (689 bytes)
Building wheels for collected packages: pytorch
  Building wheel for pytorch (setup.py) ... error
  ERROR: Failed building wheel for pytorch
  Running setup.py clean for pytorch
Failed to build pytorch
Installing collected packages: pytorch
    Running setup.py install for pytorch ... error
'''