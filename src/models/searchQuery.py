__author__ = 'Ryan'


class SearchQuery:
	"""
	This class holds information for a complete search on a specific site.

	It represents an executed query, along with references to all of the 
	results returned for that search query on the site.

	Params:
		searchModule: the searchModule that executed the query.
		searchParams: the parameters passed with HTTP request to obtain results

	"""
	def __init__(self, searchModule, searchParams):
		self.searchModule = searchModule
		self.searchParams = searchParams
		self.results = []
		self.numResults = 0

	def addResultItem(self, result):
		self.results.append(result)
		self.numResults += 1

