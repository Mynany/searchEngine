Environment: python3

install urllib
install BeautifulSoup4
install fake-useragent

final_project
	-src
		-IndexRetrival.py  ---  vector space model
		-PageRank.py  ---  pagerank algorithm
		-preprocess.py  ---  preprocess the pages
		-WebCrawler.py  --- scraping pages
	-output
		-pages  ---  output of WebCrawler, pages downloaded from website
		-preprocess
		-preprocess1  --- output of preprocess.py, processed pages
		-index_doc  ---  data structure for pages
		-index_query  --- data structure for query
		-search  ---  the query
		-finalrank  ---  the PageRank of pages
		-graph  ---  pages and their outlinks
		-match_index_num  --- match document number with link
	-outputquery  ---  ranking of using vector space model
	-result_and_compare  ---  final result 
	-report 

entry: src/IndexRetrival.py
you can run WebCrawler.py, PageRank.py, preprocess.py as well even thought the output of these 3 file is already exited



