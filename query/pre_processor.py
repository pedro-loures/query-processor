
import nltk
nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet 
from nltk.stem import WordNetLemmatizer


    
STOPWORDS = stopwords.words('english')
# create an object of class PorterStemmer
porter = PorterStemmer()
snowball = SnowballStemmer(language='english') # Faster then porter
lemmatizer = WordNetLemmatizer()



# DEFINES
# WORD_TREATMENT = ',;:_()\'"”“’[]–-+\\/'
WORD_TREATMENT = '0123456789)-–_=+§!@#$%¨&*(´`^~{}[]:;?/,<.>|\\\'\"”“’°ºª'
WORD_TREATMENT = ')-–_=+§!@#$%¨&*(´`^~{}[]:;?/,<.>|\\\'\"”“’°ºª'

    

 

def lemmatize_text(text):
    lemmatized_text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

    return lemmatized_text

def expand_common_words(query, expand=False):
    # query = query.split(' ')


    with open('bases/commom_lexicon', 'r') as common_lexicon_file:
        common_lexicon = common_lexicon_file.readlines()
    
    words =[]
    for word_query in query:
        for word_lexicon in common_lexicon:
            
            if word_lexicon[:-1] in word_query:
                words.append(' ' + word_lexicon[:-1] + ' ')
    
    
    text = ' '.join(query)

    added_text = ' '.join(words)
    return text + added_text
def expand_query(query, expand=False):
    '''
    GPT function to do query expansion
    add lemmatization
    add commom queries
    '''
    expanded_query = []
    for term in query:
        synonyms = wordnet.synsets(term)
        if synonyms and expand:
            # Add synonyms
            synonym = synonyms[0].lemmas()[0].name()
            expanded_query.append(synonym)
            
            # Add hypernyms
            # hypernyms = synonyms[0].hypernyms()
            # for hypernym in hypernyms:
            #     expanded_query.append(hypernym.lemmas()[0].name())
            
            # # Add hyponyms
            # hyponyms = synonyms[0].hyponyms()
            # for hyponym in hyponyms:
            #     expanded_query.append(hyponym.lemmas()[0].name())
            
            # Add Common Words
            common_words = expand_common_words(query)
            expanded_query.append(common_words)

            expanded_query.append(term)

        else:
            expanded_query.append(term)
            
    text =  ' '.join(expanded_query)
    # text = expand_common_words(text.split(' '))
    # text = text + ' ' + lemmatize_text(text)

    # text_set = set(text.split(' '))
    # text = ' '.join(text_set)

    return text

def expand_queries(queries_file, expand=False):
    queries_wrapper = open(queries_file, 'r')

    queries_dictionary = {}
    for line_number, csv_line in enumerate(queries_wrapper):
        if line_number == 0:
           continue
        
        query_id, text = csv_line.split(',', 1)
        
        queries_dictionary[query_id] = expand_query(text.split(' '), expand)
    
    queries_wrapper.close()
    return queries_dictionary


def get_avarage_document_length(index_path):
    ''' 
    calculates avarage document length
    and returns:
     - dict with document length
     - number of documents
     - total lenght of documents
     - avarage document length
    '''

    document_length_dict = {}
    total_document_length = 0
    with open(index_path + 'document_index','r') as document_index:
        for line_number, line in enumerate(document_index):
            docid, document_length = line.split(':')
            document_length_dict[docid] = int(document_length)
            total_document_length += int(document_length)
    avarage_document_length = total_document_length / line_number
    
    number_of_documents = line_number 
    print(number_of_documents , total_document_length, avarage_document_length)
    return document_length_dict, number_of_documents , total_document_length, avarage_document_length

    
def read_lexicon(index_path, keyword=''):
    ''''
    Reads Lexicon and return a dict with the position of each word on the inverted list
    '''
    lexicon_file = open(index_path + 'lexicon' + keyword, 'r')
    lexicon = {}
    previous_line = lexicon_file.readline()
    for line in lexicon_file:

        word, location = line.split(':')
        previous_word, previous_location = previous_line.split(':')
        lexicon[word] = int(previous_location)
        previous_line = line
    lexicon_file.close()
    return lexicon

def process_queries(queries_dictionary):
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



    for query_id in queries_dictionary.keys():


        tokenized_text= treat_text(queries_dictionary[query_id])
        queries_dictionary[query_id] = tokenized_text
    

    return queries_dictionary



def treat_text(text):
    '''
    receives the json text line, apply treatment and writes a list of words per document and return the queryID and tokenized text

    treatment:
        - split on spaces
        - eliminates nullwords ('', '\n')
        - eliminate punctuation if its the last charatcter of a word
        - eliminate stopwords
        - apply stemming (!!!taking too slow!!!)
    '''
    text = text.lower()
    for character in WORD_TREATMENT:
        text = text.replace(character, '')
    

    tokenized_text = text.split(' ')
    tokenized_text = [word for word in tokenized_text if word != '']
    # tokenized_text = ['\n'+word if word != '\n' else word for word in tokenized_text]
    tokenized_text = [word[:-1] if word[:-1].isalnum() and not word[-1].isalnum()  else  word for word in tokenized_text]
    tokenized_text = [word for word in tokenized_text if word not in STOPWORDS]   
    tokenized_text = [word for word in tokenized_text if word != '\n']   
    tokenized_text = stemming(tokenized_text)
    words = set(tokenized_text)

    return tokenized_text


def stemming(list_of_words):
  '''
  treat a list of words by stemming them
  '''
  new_list_of_words = []
  for word in list_of_words:
    new_list_of_words.append(snowball.stem(word))
  return new_list_of_words
