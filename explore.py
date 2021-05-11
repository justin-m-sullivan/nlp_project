import os
import pandas as pd
import prepare
import re 
from wordcloud import WordCloud
from bs4 import BeautifulSoup

def get_words(text):
    '''
    '''
    words = re.sub(r'[^\w\s]', '', text).split()
    return [word for word in words]



