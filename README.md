# CrossSearchCrawler [![Build Status](https://travis-ci.org/rywils21/CrossSearchCrawler.svg?branch=master)](https://travis-ci.org/rywils21/CrossSearchCrawler)

CrossSearchCrawler began as a web crawler for IEEE xplore and ACM digital libraries. It is much much easier to traverse those sites manually and download the citation information from searches. Thus, this tool is now just a citation data aggregation and analysis tool for searches from IEEE xplore.

# Usage
Starting from scratch? Build the entire database and generate all reports by executing this command from the src folder of this project:

'''bash
	python main.py do-everything ../searchesFrom_1998
'''

Of course, substitute the python call with the call to run python files on your machine. 

searchesFrom_1998 is a folder that contains data files downloaded from IEEE xplore. You can of course use any CSV files downloaded from there as your source. More on that later.


Other commands that are available are:


'''bash
	python main.py report-crossover
'''

This command does not load any files. It simply generates a crossover report of all the data currently populated in the database.


'''bash
	python main.py report-by-year
'''

This command does not load any files. It simply generates a report showing how many results there were for each search query compared to years.


'''bash
	python main.py report-by-authors
'''

This command does not load any files. It simply generates a report showing the count of contributing authors for each search query.


'''bash
	python main.py compile-folder /path/to/folder/ /output/file/name/
'''

This command is used to compile a folder of small CSV files into a single larger CSV file. This was created in order to compile search results from multiple files that were produced from the same search. This is needed when a single search returns more than 2,000 results, and results must be downloaded page by page.




