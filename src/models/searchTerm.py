__author__ = 'Ryan'


class SearchTerm:
	"""
	This class represents a search term object. It will hold
	information for a complete search on a specific site.

	It will also be a map to all of the results returned for that site.
	"""
	def __init__(self, site, terms):
		self.site = site
		self.terms = terms
		self.results = []

	"""
	Uses self.site to execute a search for this searchTerm object.
	Passes own terms to the site to execute.

	Stores the search results in self.results
	"""
	def executesearch(self):
		self.results = self.site.executesearch(self.terms)
