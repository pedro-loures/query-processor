

def get_nqi(query_document_dict, qi):
    # TODO
    return None

def calculate_IDF(N, word_document_dict, qi):
    # TODO
    '''
    calculates inverse document frequency with the formula : 
    given a query Q, containing keyword q_{1}, q_{2}, q_{n}

    {\displaystyle {\text{IDF}}(q_{i})=\ln \left({\frac {N-n(q_{i})+0.5}{n(q_{i})+0.5}}+1\right)}
    where N is the total number of documents, n(q_{i}) is the number of documents containing q_{i}
    '''
    
    IDF = None
    nqi = get_nqi(word_document_dict, qi)
    upper_fraction = N - nqi + 0.5

    return IDF

def calculate_BM25(query_document_dict):
    '''
    Given a query Q, containing keywords q_1, ..., q_n, 
    calculates the BM25 score of a document D by:

    {\displaystyle {\text{score}}(D,Q)=\sum _{i=1}^{n}{\text{IDF}}(q_{i})\cdot {\frac {f(q_{i},D)\cdot (k_{1}+1)}{f(q_{i},D)+k_{1}\cdot \left(1-b+b\cdot {\frac {|D|}{\text{avgdl}}}\right)}}}

    where 
    - f(q_i, D) is the number of times q_i occurs in the document D, 
    - |D| is the length of D in words and 
    - avgdl is the avarage document legth
    k_1 and b are free parameters usualy chosen in absense of optimization as
    k_1 \in [1.2,2.0] and b = 0.75
    - IDF is the inverse document frequency 
    '''
    pass

def rank(query_document_dict):
    query = list(query_document_dict.keys())
    for term in query:
        print(query_document_dict[term].keys())