import pandas as pd

import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import warnings
warnings.filter="ignore"

import acquire

from bs4 import BeautifulSoup

def basic_clean(text):
    '''
    This function takes in a string of text and cleans it for NLP by:
    - converting all chracters to lowercase
    - normalizing unicode characters
    - removing any characters that are not letters, numbers, single quote, or space
    
    It returns a cleaned text string.
    '''
    
    #lowercase all characters
    text = text.lower()
    
    #normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    
    #remove any characters that are not a letter, number, or single quote
    text = re.sub(r"[^a-z0-9'\s]", '', text)
    
    return text


def tokenize(text):
    '''
    This function takes in a single arguement, a string 
    and prepares it for NLP by tokenizing the words.
    
    It returns a string. 
    '''
    
    #Create the tokenizer object
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    #Use the tokenizer
    text = tokenizer.tokenize(text, return_str = True)
    
    return text

def stem(text):
    '''
    This function takes in a string as an arguement
    and stems the words for NLP.
    It returns a single string of the stemmed words. 
    '''
    #create the porter stemmer
    ps = nltk.porter.PorterStemmer()
    
    #Apply the stemmer to each word in string
    stems = [ps.stem(word) for word in text.split()]
    
    #Join the stemmed list of words back into a string
    text_stemmed = ' '.join(stems)
    
    return text_stemmed

def lemmatize(text):
    '''
    This function takes in a string of text as
    an arguement and lemmatizes the words for NLP.
    It returns a single single string of the lemmatized words.
    '''
    #create the word nest list
    wnl = nltk.stem.WordNetLemmatizer()
    
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    
    text_lemmatized = ' '.join(lemmas)
    
    return text_lemmatized

def remove_stopwords(text, extra_words=[], exclude_words=[]):
    '''
    This function takes in three arguements:
    1. A string
    2. extra_words=[] that should also be removed in addition to the std. stopwords.
    3. exclude_words=[] to signify std. stopwords that should not be removed.
    
    It returns a string with stopwords removed.
    '''
    stopword_list = stopwords.words('english')
    
    if len(extra_words) > 0:
        stopword_list.append(extra_words)
    else:
        stopword_list = stopword_list
        
    if len(exclude_words) > 0:
        stopword_list.remove(exclude_words)
    
    words = text.split()
    
    filtered_words = [word for word in words if word not in stopword_list]
    
    text_without_stopwords = ' '.join(filtered_words)
    
    return text_without_stopwords

