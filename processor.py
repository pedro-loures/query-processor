    

# External Import
import sys
import argparse
import time 

# Internal Import 
import rankers.BM25 as bm25
import rankers.TDIDF as tdidf
import query.matching as matching
import query.pre_processor as pp




def main():


    """
    Your main calls should be added here
    """
    start_time = time.time()


    # print('----- PART 1 Process queries ------')
    part_time = time.time()
    queries_dictionary = pp.process_queries(args.query_file)
    end_time = time.time()
    timeof_part1 = end_time - part_time
    # print('time = ' +  str(end_time - part_time) )

    # print('----- PART 2 Get Avarage document_length ------')
    part_time = time.time()
    sizeof_collection, colection_length, avarage_document_length = pp.get_avarage_document_length(args.index_file)
    end_time = time.time()
    timeof_part2 = end_time - part_time
    # print('time = ' +  str(end_time - part_time) )



    # print(queries_dictionary)
    timeof_part3 = 0
    timeof_part4 = 0
    for query_id in queries_dictionary:
        # print('----- PART 3 create dict from index line  ------')
        part_time = time.time()
        word_document_dict = matching.create_dict_from_index_line(args.index_file, queries_dictionary[query_id] )
        end_time = time.time()
        timeof_part3 += end_time - part_time
        # print('time = ' +  str(end_time - part_time) )

        # print('----- PART 4 calculate term relative frequency  ------')
        part_time = time.time()
        word_document_dict = matching.update_document_length(args.index_file, word_document_dict)
        end_time = time.time()
        timeof_part4 += end_time - part_time
        # print('time = ' +  str(end_time - part_time) )


    print('----- PART 1 Process queries ------')
    print('time = ' +  str(timeof_part1) )
    print('----- PART 2 Get Avarage document length ------')
    print('time = ' +  str(timeof_part2) )
    print('----- PART 3 create dict from index line  ------')
    print('time = ' +  str(timeof_part2) )
    print('----- PART 4 calculate term relative frequency  ------')
    print('time = ' +  str(timeof_part3) )
    
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