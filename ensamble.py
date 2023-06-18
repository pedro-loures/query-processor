

def write_rank_to_file(ranking, query_id, file):
    '''
    writes a given rank to a csv file
    '''

    for docid in ranking.keys():
        file.write(query_id + ',' +  docid + '\n')

    return 


def sum_ranks(ranking1, ranking2, weight = .75):
    
    # normalize scores
    max_ranking1 = max(ranking1.values())
    # print('before: max_ranking1:', max_ranking1)
    for key in ranking1.keys():
        ranking1[key] = ranking1[key] / max_ranking1  * 1-weight
    max_ranking1 = max(ranking1.values())
    # print('after: max_ranking1:', max_ranking1)
    
    max_ranking2 = max(ranking2.values())
    # print('before: max_ranking2:', max_ranking2)
    for key in ranking2.keys():
        ranking2[key] = (ranking2[key]) / (max_ranking2 ) * weight
    max_ranking2 = max(ranking2.values())
    # print('after: max_ranking2:', max_ranking2)

    documents = set(list(ranking1.keys())+ list(ranking2.keys()))
    new_rank = {}
    for document in documents:
        
        if document in ranking1 and document in ranking2:
            new_rank[document] = ranking1[document] + ranking2[document]
        elif document in ranking1:
            new_rank[document] = ranking1[document]
        elif document in ranking2:
            new_rank[document] = ranking2[document]

    sorted_new_rank = sorted(new_rank.items(), key=lambda x:x[1], reverse=True)
    # print(sorted_new_rank)
    return dict(sorted_new_rank)