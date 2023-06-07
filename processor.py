    

# External Import
import sys
import argparse




def main():


    """
    Your main calls should be added here
    """
    print('ok')

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
    
if __name__ == "__main__":
    main()