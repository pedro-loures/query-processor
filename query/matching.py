


import os

def get_documents(index_file, line):
    '''
    Given a line and index_file returns a dict with 
    the word in this line, the documents that contain it
    and the term absolute frequency in this document
    '''
    index_file.seek(0)
    word_document_dict = {}
    for line_number, line_text in enumerate(index_file):
        if line_number == line + 1:
            word, documents = line_text.split(':')
            documents = documents.split(';')[:-1]
            for document in documents:
                # print(document)
                document, frequency = document.split(',')
                word_document_dict[document]=frequency
            return word_document_dict



def create_dict_from_index_line(index_path, query):
    '''
    given an index and a query it get the documents
    that contain each word in the query and how many
    times that word is in the document
    returs {word:{documents:frequency}}
    '''
    query = sorted(query)

    lexicon = open(index_path + 'lexicon', 'r')
    index = open(index_path + 'index', 'r')

    print(query)
    query_word = query.pop(0)
    query_dict = {}
    for word_id, word in enumerate(lexicon):
        word = word.replace('\n', '')    
        if word == query_word:
            index.seek(word_id+1)
            word_document_dict = get_documents(index, word_id)
            query_dict[word] =word_document_dict
            if len(query) == 0: break
            query_word = query.pop(0)
    index.close()
    lexicon.close()
    return query_dict

def find_document_length(document_index, document):
    '''
    finds document length in document index
    '''
    document_file = ''
    while(document != document_file):
        document_index_line = next(document_index)
        document_file, document_length = document_index_line.split(':')
    return int(document_length)
        # print(document_file, document)

def update_document_length(index_path, word_document_dict):
    '''
    calculates term relative frequency by comparing to the size of 
    the document in index_path+document_indexer

    Returns docuemn
    '''

    document_index = open(index_path + 'document_index', 'r')
    for entry in word_document_dict:
        document_index.seek(0   )
        documents_keys = sorted(word_document_dict[entry])
        # print(documents_keys)
        for document in documents_keys:
            document_length = find_document_length(document_index, document)    
            word_document_dict[entry][document]=word_document_dict[entry][document] , document_length,

    # print(word_document_dict)
    document_index.close()
    return word_document_dict