__author__ = 'Ryan'


import json


class SearchEngineSite:
	"""
	This is an object that contains a definition of a site to search from.

	It contains the URL and search input field names, as well as search result
	list item names in order to execute searches and retrieve results over HTTP.
	"""
	def __init__(self, url, searchFields, resultListName, resultItemDef, resultsPerPage, pageNumber, numberOfResults):
		self.url = url
		self.searchFields = searchFields
		self.resultListName = resultListName
		self.resultItemDef = resultItemDef
		self.resultsPerPage = resultsPerPage
		self.pageNumber = pageNumber
		self.numberOfResults = numberOfResults

	"""
	Executes a search for the given terms.
	"""
	def executesearch(self, terms):
		    # This is just a proof of concept that the acm can be searched programatically.
	    with session() as s:
	        response = s.get("http://dl.acm.org/advsearch.cfm?coll=DL&dl=ACM&CFID=553218618&CFTOKEN=75971898")
	        # Get a beautiful soup object for this page
	        soup = BeautifulSoup(response.text, "html.parser")
	        print(soup.prettify().encode('utf8'))

	        search = {"allofem" : '"Intrusion Detection System"'}
	        response = s.get("http://dl.acm.org/advsearch.cfm?coll=DL&dl=ACM&CFID=553218618&CFTOKEN=75971898", params=search)
	        soup = BeautifulSoup(response.text, "html.parser")
	        print("\n\n\n====================\n\n")
	        print(soup.prettify().encode('utf8'))


def parseSearchEngineJSON(definitionFilePath):
	pass
