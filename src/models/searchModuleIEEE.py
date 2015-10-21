__author__ = 'Ryan'


from requests import session
from bs4 import BeautifulSoup


class IEEESearchEngine:
	"""
	This is an object that is able to search and get results from a search on
	IEEE Xplore.

	It contains the URL to get the search results and the parameters required
	to execute that search.

	Params:
		searchTerms: a dictionary of categories (keys) to lists (values) of search terms
		globalResults: a reference to a global set of search results 
					   with unique titles, authors, and identifiers (DOI)

	Important query items:
		1. self.params['queryText'] is the value that must hold the search query
			the value must be a string that begins and ends with parentheses
			i.e. queryText=(Intrusion Detection System)

		2. self.params['refinements'] holds a list with two strings.
			This is to refine results by conference publications and journals and magazines.
			Both strings must be sent as params to refinements in a request.

		3. self.params['rowsPerPage'] is the value controlling how many results appear per request
			Currently set to 100,000. Must check if a search goes beyond 100,000 results.
	"""
	def __init__(self, searchTerms, globalResults):
		self.url = "http://ieeexplore.ieee.org/search/searchresult.jsp"
		self.params = { "action" : "search", \
						"searchField" : "Search_All", \
						"matchBoolean" : "true", \
						"queryText" : "", \
						"refinements" : ["4291944822", "4291944246"], \
						"ranges" : "2009_2016_Year", \
						"rowsPerPage" : "100000" \
					  }
		self.searchTerms = searchTerms

	"""
	Executes a search for the given query

	Returns: a parsed beautiful soup page of the results page.
	"""
	def executeSearch(self, query):
		self.params['queryText'] = query
        response = requests.get(self.url, self.params)
        # Get a beautiful soup object for this page
        return BeautifulSoup(response.text, "html.parser")