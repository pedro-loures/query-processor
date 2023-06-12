    

# External Import
import sys
import argparse

# Internal Import 
import rankers.BM25 as bm25
import rankers.TDIDF as tdidf
import query.matching as matching
import query.pre_processor as pp




def main():


    """
    Your main calls should be added here
    """
    queries_dictionary = pp.process_queries(args.query_file)


    print(queries_dictionary)
    for query_id in queries_dictionary:
        word_document_dict = matching.create_dict_from_index_line(args.index_file, queries_dictionary[query_id] )
        matching.calculate_term_relative_frequncy(args.index_file, word_document_dict)

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