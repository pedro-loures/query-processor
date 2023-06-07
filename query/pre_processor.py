# todo list pre-processor
# TODO 0 create query processosr



# TODO 0.0 word treatment
# TODO 0.1 return dict

import nltk
from nltk.tokenize import word_tokenize
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from functools import reduce

STOPWORDS = stopwords.words('english')
# create an object of class PorterStemmer
porter = PorterStemmer()
snowball = SnowballStemmer(language='english') # Faster then porter



# DEFINES
# WORD_TREATMENT = ',;:_()\'"”“’[]–-+\\/'
WORD_TREATMENT = '0123456789)-–_=+§!@#$%¨&*(´`^~{}[]:;?/,<.>|\\\'\"”“’°ºª'



def process_queries(query_file):
    '''
    given a query csv file (query_id, query) 
    
    appply treatment:
        - split on spaces
        - eliminates nullwords ('')
        - eliminate punctuation if its the last charatcter of a word
        - eliminate stopwords
        - apply stemming (!!!taking too slow!!!)
   
    and returns a dict query_id, query
    '''
    queries_wrapper = open(query_file, 'r')

    queries_dictionary = {}
    for line_number, query in enumerate(queries_wrapper):
        if line_number == 0:
           continue

        query_id, tokenized_text= treat_text(query)
        queries_dictionary[query_id] = tokenized_text
    
    queries_wrapper.close()
    return queries_dictionary



def treat_text(csv_line):
    '''
    receives the json text line, apply treatment and writes a list of words per document and return the queryID and tokenized text

    treatment:
        - split on spaces
        - eliminates nullwords ('')
        - eliminate punctuation if its the last charatcter of a word
        - eliminate stopwords
        - apply stemming (!!!taking too slow!!!)
    '''
    query_id, text = csv_line.split(',', 1)
    text = text.lower()
    for character in WORD_TREATMENT:
        text = text.replace(character, '')
    
    

    tokenized_text = text.split(' ')
    tokenized_text = [word for word in tokenized_text if word != '']
    # tokenized_text = ['\n'+word if word != '\n' else word for word in tokenized_text]
    tokenized_text = [word[:-1] if word[:-1].isalnum() and not word[-1].isalnum()  else  word for word in tokenized_text]
    tokenized_text = [word for word in tokenized_text if word not in STOPWORDS]   
    tokenized_text = stemming(tokenized_text)
    words = set(tokenized_text)

    return query_id, tokenized_text


def stemming(list_of_words):
  '''
  treat a list of words by stemming them
  '''
  new_list_of_words = []
  for word in list_of_words:
    new_list_of_words.append(snowball.stem(word))
  return new_list_of_words
