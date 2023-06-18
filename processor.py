    

# External Import
import sys
import argparse
import time 

# Internal Import 
import rankers.BM25 as bm25
import rankers.TDIDF as tdidf
import query.matching as matching
import query.pre_processor as pp
import ensamble



def main():
    start_time = time.time()
    file = open('result/ranking.csv', 'w')
    file.write('QueryId,EntityId\n'   )

    # print('----- PART 0 query expansion ------')
    part_time = time.time()
    queries_dictionary = pp.expand_queries(args.query_file)
    end_time = time.time()
    timeof_part0 = end_time - part_time
    # print('time = ' +  str(end_time - part_time) )




    # print('----- PART 1 Process queries ------')
    part_time = time.time()
    queries_dictionary = pp.process_queries(queries_dictionary)
    end_time = time.time()
    timeof_part1 = end_time - part_time
    # print('time = ' +  str(end_time - part_time) )




    # print('----- PART 2 Get Avarage document_length ------')
    part_time = time.time()
    document_index, sizeof_collection, colection_length, avarage_document_length = pp.get_avarage_document_length(args.index_file)
    end_time = time.time()
    timeof_part2 = end_time - part_time
    # print('time = ' +  str(end_time - part_time) )




    # print('----- PART 3.1 Read Lexicon ------')
    part_time = time.time()
    lexicon = pp.read_lexicon(args.index_file)
    end_time = time.time()
    timeof_part3 = end_time - part_time
    # print('time = ' +  str(end_time - part_time) )
    
    # print('----- PART 3.2 Read Lexicon ------')
    part_time = time.time()
    lexicon_keyword = pp.read_lexicon(args.index_file, keyword = '_keyword')
    end_time = time.time()
    timeof_part3 = end_time - part_time
    # print('time = ' +  str(end_time - part_time) )




    # print(queries_dictionary)
    timeof_part4 = 0
    timeof_part5 = 0
    timeof_part6 = 0
    timeof_part7 = 0
    timeof_part_final = 0
    for query_id in queries_dictionary:
        # print('----- PART 4.1 create dict from index line  ------')
        part_time = time.time()
        query_document_dict = matching.create_dict_from_index_line(args.index_file, queries_dictionary[query_id], lexicon)
        end_time = time.time()
        timeof_part4 += end_time - part_time
        # print('time = ' +  str(end_time - part_time) )

        # print('----- PART 4.2 create dict from index keyword line  ------')
        part_time = time.time()
        query_keyword_dict = matching.create_dict_from_index_line(args.index_file, queries_dictionary[query_id], lexicon_keyword, keyword='_keyword')
        end_time = time.time()
        timeof_part4 += end_time - part_time
        # print('time = ' +  str(end_time - part_time) )




        # print('----- PART 5.1 calculate term relative frequency  ------')
        part_time = time.time()
        query_document_dict = matching.update_document_length(document_index, query_document_dict)
        end_time = time.time()
        timeof_part5 += end_time - part_time
        # print('time = ' +  str(end_time - part_time) )

        # print('----- PART 5.2 calculate term keyword relative frequency  ------')
        part_time = time.time()
        query_keyword_dict = matching.update_document_length(document_index, query_keyword_dict)
        end_time = time.time()
        timeof_part5 += end_time - part_time
        # print('time = ' +  str(end_time - part_time) )




        # print('----- PART 6.1 rank using bm25  ------')
        part_time = time.time()
        ranking = bm25.rank(query_document_dict, document_index, sizeof_collection, avarage_document_length)
        end_time = time.time()
        timeof_part6 += end_time - part_time
        # print('time = ' +  str(end_time - part_time) )

        # print('----- PART 6.2 rank using bm25  ------')
        part_time = time.time()
        ranking_keywords = bm25.rank(query_keyword_dict, document_index, sizeof_collection, avarage_document_length)
        end_time = time.time()
        timeof_part6 += end_time - part_time
        # print('time = ' +  str(end_time - part_time) )


        

        # print('----- PART 7 summing ranks  ------')
        part_time = time.time()
        ranking = ensamble.sum_ranks(ranking, ranking_keywords, weight = .5)
        end_time = time.time()
        timeof_part7 += end_time - part_time
        # print('time = ' +  str(end_time - part_time) )


        

        # print('----- FINAL Writing rank to document  ------')
        part_time = time.time()
        ensamble.write_rank_to_file(ranking, query_id, file)
        end_time = time.time()
        timeof_part_final += end_time - part_time
        # print('time = ' +  str(end_time - part_time) )

    print('----- PART Query Expansion ------')
    print('time = ' +  str(timeof_part0) )
    print('----- PART 1 Process queries ------')
    print('time = ' +  str(timeof_part1) )
    print('----- PART 2 Get Avarage document length ------')
    print('time = ' +  str(timeof_part2) )
    print('----- PART 3 Read Lexicon ------')
    print('time = ' +  str(timeof_part3) )
    print('----- PART 4 create dict from index line  ------')
    print('time = ' +  str(timeof_part4) )
    print('----- PART 5 calculate term relative frequency  ------')
    print('time = ' +  str(timeof_part5) )
    print('----- PART 6 rank using bm25  ------')
    print('time = ' +  str(timeof_part6) )
    print('----- PART 7 summing ranks  ------')
    print('time = ' +  str(timeof_part7) )
    print('----- FINAL Writing rank to document  ------')
    print('time = ' +  str(timeof_part_final) )
    
    file.close()
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    
    
    
    # Query File
    parser.add_argument(
		'-q',
		dest='query_file',
		action='store',
		required=True,
		type=str,
		help='path to query files'
	)
	# Index File
    parser.add_argument(
		'-i',
		dest='index_file',
		action='store',
		required=True,
		type=str,
		help='index file path'
	)
    #M Ranker Type file
    parser.add_argument(
        '-r',
        dest='ranker',
        action='store',
        required=True,
        type=str,
        help='ranker should be BM25 or TFIDF'
    )

    args = parser.parse_args()
    main()