

import linecache
import os

import query.pre_processor as pp

def get_documents(index_file, location):
    '''
    Given a line and index_file returns a dict with 
    the word in this line, the documents that contain it
    and the term absolute frequency in this document
    '''
    # index_file.seek(0)
    word_document_dict = {}

    # print(location, int(location))
    index_file.seek(location,0)
    line_text = index_file.readline()

    word, documents = line_text.split(':')
    # print(word)
    documents = documents.split(';')[:-1]
    for document in documents:
        # print(document)
        document, frequency = document.split(',')
        word_document_dict[document]=frequency
    return word_document_dict



def create_dict_from_index_line(index_path, query, lexicon, keyword = ''):
    '''
    given an index and a query it get the documents
    that contain each word in the query and how many
    times that word is in the document
    returs {word:{documents:frequency}}
    '''
    query = sorted(query)

    # lexicon = open(index_path + 'lexicon', 'r')
    index = open(index_path + 'index' + keyword, 'r')

    # print(query)
    query_dict = {}
    while True:
        for word in query:
            if word in lexicon:
                word_document_dict = get_documents(index,lexicon[word])
                query_dict[word] =word_document_dict


        documents = set()
        for term in query:
            documents.update(query_dict[term].keys())


        if len(documents) >= 100:
            break  
        print('findin more documents for query:', query)
        query = pp.expand_common_words(query)
        query = [word for word in query.split(' ') if word != '']


    assert len(documents) >= 100, 'could not find enough relevant documents'
    index.close()

    return query_dict

# def find_document_length(document_index, document):
#     '''
#     finds document length in document index
#     '''
#     document_file = ''
#     while(document != document_file):
#         document_index_line = next(document_index)
#         document_file, document_length = document_index_line.split(':')
#     return int(document_length)
#         # print(document_file, document)

def update_document_length(document_index, word_document_dict):
    '''
    calculates term relative frequency by comparing to the size of 
    the document in the document_index

    Returns worrd document dict
    '''

    # document_index = open(index_path + 'document_index', 'r')
    for entry in word_document_dict:
        documents_keys = sorted(word_document_dict[entry])
        # print(documents_keys)
        for document in documents_keys:
            document_length = document_index[document]    
            word_document_dict[entry][document]=word_document_dict[entry][document] , document_length,

    # print(word_document_dict)
    # document_index.close()
    return word_document_dict

