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
						"searchField" : "Search_All_Text", \
						"matchBoolean" : "true", \
						"queryText" : "", \
						"refinements" : ["4291944822", "4291944246"], \
						"ranges" : "2009_2016_Year", \
						"rowsPerPage" : "100000" \
					  }
		self.searchTerms = searchTerms
		self.globalResults = globalResults
		self.executedQueries = []


	"""
	Crafts search queries for this module.
	Executes those search queries on the IEEE site.
	Records the results.
	"""
	def run(self):
		queries = self.craftQueries()
		for q in queries:
			resultPage = self.executeSearch(q)
			searchQuery = self.parseResults(resultPage, self.params)
			self.executedQueries.append(searchQuery)


	"""
	Crafts a set of queries to execute for this specific site.
	"""
	def craftQueries(self):
		queries = []
		groupStrings = []

		andStr = " AND "
		orStr = " OR "
		quotChar = ".QT."
		intrusionDetectionString = "(" + quotChar + "Intrusion Detection System" + quotChar + ")"

		# Create query strings for each group of search terms
		for key in self.searchTerms.keys():
			groupString = "("
			for term in self.searchTerms[key]:
				groupString += quotChar + term + quotChar + orStr
			groupString += ")"
			groupStrings.append(groupString)

		fullQuery = "(" + intrusionDetectionString

		# Craft query strings of "intrusion detection" and "group1" and "group2"
		for i in range(0, len(groupStrings)):
			# Create a fullQuery that involves every group
			fullQuery += groupStrings[i] + andStr
			for j in range(0, len(groupStrings)):
				query = "(" + intrusionDetectionString + andStr + groupStrings[i] + andStr + groupStrings[j] + ")"
				queries.append(query)

		fullQuery += ")"
		queries.append(fullQuery)

		return queries


	"""
	Executes a search for the given query

	Returns: a parsed beautiful soup page of the results page.
	"""
	def executeSearch(self, query):
		self.params['queryText'] = query
        response = requests.get(self.url, self.params)
        # Get a beautiful soup object for this page
        return BeautifulSoup(response.text)


    """
    Parses the result page from an executed search.

    Params: 
    	resultPage: a parsed BeautifulSoup object of the results page of a search
    	searchParams: the search params that were used for this search

    Returns:
    	a searchQuery object that is able to recreate the exact search, 
    	and represents the results of the search
    """
    def parseResults(self, resultPage, searchParams):
    	searchQuery = searchQuery(self, searchParams)
    	resultItems = []
    	# TODO: Get the result items from the soup object and populate the list with three-tuples
    	for node in resultPage.findall(attrs={'class': 'article-list-item'}):
    		print("Found an item")

    	# r is a three-tuple (title, authors, ID)
    	for r in resultItems:
    		if r in self.globalResults:
    			# TODO: Check this syntax with python sets
    			searchQuery.addResultItem(self.globalResults.get(r))
    		else:
    			self.globalResults.add(r)
    			searchQuery.addResultItem(r)

    	return searchQuery
