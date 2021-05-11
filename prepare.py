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
    
    # Remove 'exclude_words' from stopword_list to keep these in my text.
    stopword_list = set(stopword_list) - set(exclude_words)
    
    # Add in 'extra_words' to stopword_list.
    stopword_list = stopword_list.union(set(extra_words))
    
    words = text.split()
    
    filtered_words = [word for word in words if word not in stopword_list]
    
    text_without_stopwords = ' '.join(filtered_words)
    
    return text_without_stopwords

def prep_github_repo_df(df, n=None, extra_words=[]):
    '''
    This function takes in two areguemnets where the first is a dataframe 
    and the second is n where the value of n is equal to minimum number of
    occurances of a programming langauge required to be represented in the
    dataframe. The default is none and will keep all observations.

    The function prepares the df for NLP analysis by:
    - Dropping observations with nulls in language
    - Replacing 'jupyter notebook' in langauge with 'python'
    - Dropping any observations where the programming language is underrepresented
    - Appending the df by adding 3 additional columns:
        - A clean column where the readme_contents have undergone general cleaning and tokenization
        - A stemmed columb where the contents have been cleaned and stemmed
        - A lemmatized column where the contents have been clean and lemmatized

    It returns a single dataframe.

    '''

    #Drop observagions with missing values in language
    df = df.dropna()

    #Replace Jupyter Notebook in language with python
    df.language = df.language.replace("Jupyter Notebook", "Python")

    #Drop observations that represent a programming language that is 
    #underrepresented in the dataframe. Languages that are represented by
    #less than 7 observations will be dropped.

    #Define the value counts for languages in the dataframe
    value_counts = df['language'].value_counts()

    #Select the observations to remove based on language count representation threshold
    to_remove = value_counts[value_counts < n].index

    # Keep rows where the language column is not in to_remove if n was defined
    if n > 0:
        df = df[~df.language.isin(to_remove)]
    else:
        df = df

    #Create three additional columns on the dataframe
    #Where the readme_contents are cleaned three different ways
    #including a general clean, a stemmed version of the contents
    #and a lemmatized version of the contents

    #clean to hold the normalized and tokenized original with the stopwords removed.
    df['clean'] = df['readme_contents'].apply(lambda x: remove_stopwords(tokenize(basic_clean(x)), extra_words))

    #stemmed to hold the stemmed version of the cleaned data.
    df['stemmed'] = df['clean'].apply(lambda x: stem(x))

    #lemmatized to hold the lemmatized version of the cleaned data.
    df['lemmatized'] = df['clean'].apply(lambda x: lemmatize(x))


    return df




    

