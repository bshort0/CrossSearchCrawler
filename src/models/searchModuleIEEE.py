__author__ = 'Ryan'


import requests
from bs4 import BeautifulSoup
from models.searchQuery import SearchQuery


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
			print("Query: " + q)
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
		intrusionDetectionString = quotChar + "Intrusion detection system" + quotChar

		# Create query strings for each group of search terms
		for key in self.searchTerms.keys():
			groupString = ""
			for i in range(0, len(self.searchTerms[key])):
				if groupString == "":
					groupString = "(" + quotChar + self.searchTerms[key][i] + quotChar + ")"
				else:
					groupString = "(" + groupString + orStr + quotChar + self.searchTerms[key][i] + quotChar + ")"
			groupStrings.append(groupString)

		# Craft query strings of "intrusion detection" and "group1" and "group2"
		for i in range(0, len(groupStrings)):
			# Create a fullQuery that involves every group
			singleQuery = "(" + groupStrings[i] + andStr + intrusionDetectionString + ")"
			queries.append(singleQuery)
			for j in range((i+1), len(groupStrings)):
				query = "(" + intrusionDetectionString + andStr + groupStrings[i] + andStr + groupStrings[j] + ")"
				queries.append(query)

		return queries


	"""
	Executes a search for the given query

	Returns: a parsed beautiful soup page of the results page.
	"""
	def executeSearch(self, query):
		self.params['queryText'] = query
		response = requests.get(self.url, params=self.params)
		print("URL: " + response.url)
		print("Text: " + response.text)
		# Get a beautiful soup object for this page
		soup = BeautifulSoup(response.text, "html.parser")
		return soup


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

		# print(resultPage.prettify().encode('utf8'))

		search = SearchQuery(self, searchParams)
		resultItems = []

		if resultPage == None:
			print("result Page is none")

		# TODO: Get the list items somehow
		for node in resultPage.find_all("li"):
			print("Found an item")

		# r is a three-tuple (title, authors, ID)
		for r in resultItems:
			if r in self.globalResults:
				# TODO: Check this syntax with python sets
				search.addResultItem(self.globalResults.get(r))
			else:
				self.globalResults.add(r)
				search.addResultItem(r)

		return search
