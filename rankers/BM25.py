import math


def calculate_IDF(N, nqi):
    # TODO
    '''
    calculates inverse document frequency with the formula : 
    given a query Q, containing keyword q_{1}, q_{2}, q_{n}

    {\displaystyle {\text{IDF}}(q_{i})=\ln \left({\frac {N-n(q_{i})+0.5}{n(q_{i})+0.5}}+1\right)}
    where 
    - N is the total number of documents, 
    - n(q_{i}) is the number of documents containing q_{i}
    '''
    


    numerator = N - nqi + 0.5
    denominator = nqi + 0.5

    return math.log(numerator/denominator + 1)

def calculate_BM25(query, document, avgdl, f_,documents_per_query, sizeof_collection, k1=1.5, b=0.75):
    '''
    Given a query, containing keywords q_1, ..., q_n, 
    calculates the BM25 score of a document D by:

    score(D,query) = sum( IDF(term) * f_term_document * (k1 + 1) / (f_term_D + k1 * ( 1 - b + b *sizeof_document / avgdl))   
    
        where 
    - f_term_document is the number of times a term occurs in the document D, 
    - sizeof_document is the length of D in words and 
    - avgdl is the avarage document legth
    - k1 and b are free parameters usualy chosen in absense of optimization as
        k1 \in [1.2,2.0] and b = 0.75
    - IDF is the inverse document frequency 
    '''
    

    summation = 0 
    for term in query:
        if document not in f_[term]:
            continue

        f_term_document, sizeof_document = f_[term][document] 
        f_term_document = int(f_term_document)
        IDF = calculate_IDF(sizeof_collection, documents_per_query[term])
        numerator = f_term_document * (k1 + 1)
        denominator = f_term_document + k1 *(1-b+b*sizeof_document/avgdl)
        summation += IDF* numerator/denominator
    return summation

def get_document_size():
    return 0

def rank(query_document_dict,  
         index_path,
         sizeof_collection, 
         avarage_document_length):
    query = list(query_document_dict.keys())
    documents = set()
    documents_per_query = {}
    for term in query:
        documents_per_query[term] = len(query_document_dict[term].keys())
        documents.update(query_document_dict[term].keys() )
    documents = sorted(documents)


    document_index_wrapper = open(index_path + 'document_index', 'r')
    ranking = []
    for document in documents:        
        ranking.append((document, calculate_BM25(query,
                                                document,
                                                avarage_document_length,
                                                query_document_dict,
                                                documents_per_query,
                                                sizeof_collection)))
    ranking.sort(key= lambda x:x[1], reverse=True)
    document_index_wrapper.close()
    # assert len(ranking) >= 100, 'could not find enough relevant documents'
    return ranking[:100]
    
