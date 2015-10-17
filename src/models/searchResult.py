__author__ = 'Ryan'


class SearchResult:
	"""
	Object that represents one result item of a search.

	In this case it will represent the title, authors, and DOI of research papers.
	"""
	def __init__(self, title, authors, identification):
		self.title = title
		self.authors = authors
		self.doi = identification
