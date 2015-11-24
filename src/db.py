
import sqlite3

class DBManager:
	def __init__(self, connection="searches.db"):
		self.conn = sqlite3.connect(connection)
		self.cursor = self.conn.cursor()

		self.initializeTables()

	def initializeTables(self):
		tableCommands = ['''CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY, name text)''', \
						 '''CREATE TABLE IF NOT EXISTS publications (id INTEGER PRIMARY KEY, title text, year text, doi text, isbn text, issn text, url text, startpage text, endpage text)''', \
						 '''CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, name text)''', \
						 '''CREATE TABLE IF NOT EXISTS authorpublink (authorID INTEGER, pubID INTEGER)''', \
						 '''CREATE TABLE IF NOT EXISTS tagpublink (tagID INTEGER, pubID INTEGER)''', \
						 '''CREATE TABLE IF NOT EXISTS searches (id INTEGER PRIMARY KEY, searchText text, site text)''', \
						 '''CREATE TABLE IF NOT EXISTS searchpublink (searchID INTEGER, pubID INTEGER)'''
						]
		for command in tableCommands:
			self.cursor.execute(command)

	def putSearchResults(self, searchDetails, entries):

		searchID = self.putSearch(searchDetails)
		for entry in entries:
			entryID = self.putEntry(entry)
			self.putSearchLink(searchID, entryID)


	def putSearch(self, search):
		exists = False

		# Check if this search has been inserted yet
		idSql = 'SELECT id FROM searches WHERE searchText="%s" AND site="%s";' %(search['query'], search['site'])
		self.cursor.execute(idSql)
		results = self.cursor.fetchall()
		if len(results) > 0:
			exists = True

		# If it doesn't exist, insert it
		if not exists:
			sql = 'INSERT INTO searches (searchText, site) VALUES ( "%s", "%s");' %(search['query'], search['site'])
			self.cursor.execute(sql)

		# Get the ID
		self.cursor.execute(idSql)
		idVal = self.cursor.fetchone()

		return idVal[0]


	def putEntry(self, entry):
		exists = False

		idSql = 'SELECT id FROM publications WHERE title="%s" AND year="%s" AND doi="%s" AND isbn="%s" AND issn="%s" AND url="%s" AND startpage="%s" AND endpage="%s"' % (entry['Document Title'], entry['Year'], entry['DOI'], entry["ISBN"], entry["ISSN"], entry["PDF Link"], entry["Start Page"], entry["End Page"])
		self.cursor.execute(idSql)
		results = self.cursor.fetchall()

		if len(results) > 0:
			exists = True

		if not exists:
			sql = 'INSERT INTO publications (title, year, doi, isbn, issn, url, startpage, endpage) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' % (entry['Document Title'], entry['Year'], entry['DOI'], entry['ISBN'], entry['ISSN'], entry["PDF Link"], entry["Start Page"], entry["End Page"])
			self.cursor.execute(sql)

		self.cursor.execute(idSql)
		idVal = self.cursor.fetchone()

		for author in entry["Authors"].split(";"):
			authorID = self.putAuthor(author)
			self.putAuthorPubLink(authorID, idVal[0])

		return idVal[0]
		

	def putAuthor(self, authorName):
		exists = False

		# Check if this search has been inserted yet
		idSql = 'SELECT id FROM authors WHERE name="%s";' %(authorName)
		self.cursor.execute(idSql)
		results = self.cursor.fetchall()
		if len(results) > 0:
			exists = True

		# If it doesn't exist, insert it
		if not exists:
			sql = 'INSERT INTO authors(name) VALUES ("%s");' %(authorName)
			self.cursor.execute(sql)

		# Get the ID
		self.cursor.execute(idSql)
		idVal = self.cursor.fetchone()

		return idVal[0]

	def putSearchLink(self, searchID, entryID):
		exists = False
		idSql = 'SELECT searchID, pubID FROM searchpublink WHERE searchID="%s" AND pubID="%s";' % (searchID, entryID)
		self.cursor.execute(idSql)
		results = self.cursor.fetchall()
		if len(results) > 0:
			exists = True

		if not exists:
			putSql = 'INSERT INTO searchpublink (searchID, pubID) VALUES ("%s", "%s");' % (searchID, entryID)
			self.cursor.execute(putSql)

	def putAuthorPubLink(self, authorID, pubID):
		exists = False
		idSql = 'SELECT authorID, pubID FROM authorpublink WHERE authorID="%s" AND pubID="%s";' % (authorID, pubID)
		self.cursor.execute(idSql)
		results = self.cursor.fetchall()
		if len(results) > 0:
			exists = True

		if not exists:
			putSql = 'INSERT INTO authorpublink (authorID, pubID) VALUES ("%s", "%s");' % (authorID, pubID)
			self.cursor.execute(putSql)


	def getSearches(self):
		sql = "SELECT id, searchText from searches;"
		self.cursor.execute(sql)

		return self.cursor.fetchall()


	"""
	This function returns a grouping of searches by year.

	The year value is in the publications table. The search query text is in the searches table.

	There is probably a more efficient way to do this in sql but I don't know how to write it.
	"""
	def getSearchesByYear(self):
		searchsql = "SELECT searchText, id from searches;"
		linksql = "SELECT searchID, pubID from searchpublink;"
		pubsql = "SELECT id, year from publications;"
		self.cursor.execute(searchsql)
		searches = self.cursor.fetchall()
		self.cursor.execute(linksql)
		links = self.cursor.fetchall()
		self.cursor.execute(pubsql)
		pubs = self.cursor.fetchall()

		years = set()
		searchesByYear = {}
		for s in searches:
			searchesByYear[s[0]] = {}
			searchID = s[1]
			pubIDs = []
			for l in links:
				if l[0] == searchID:
					pubIDs.append(l[1])
			for p in pubs:
				if p[0] in pubIDs:
					if p[1] not in searchesByYear[s[0]]:
						years.add(p[1])
						searchesByYear[s[0]][p[1]] = 0
					searchesByYear[s[0]][p[1]] += 1

		for s in searchesByYear.keys():
			for y in years:
				if y not in searchesByYear[s]:
					searchesByYear[s][y] = 0


		return searchesByYear


	def getAuthors(self):
		sql = "SELECT id, name FROM authors;"
		self.cursor.execute(sql)

		return self.cursor.fetchall()


	def getSearchesToAuthorCount(self):
		authPubSql = "SELECT authorID, pubID FROM authorpublink;"
		searchPubSql = "SELECT searchID, pubID FROM searchpublink;"

		self.cursor.execute(authPubSql)
		authLinks = self.cursor.fetchall()

		self.cursor.execute(searchPubSql)
		searchLinks = self.cursor.fetchall()

		searches = self.getSearches()

		searchCounts = {}
		for s in searches:
			searchCounts[s[1]] = set()
			for link in searchLinks:
				if link[0] == s[0]:
					for auth in authLinks:
						if link[1] == auth[1]:
							searchCounts[s[1]].add(auth[0])

		for key in searchCounts.keys():
			searchCounts[key] = len(searchCounts[key])

		return searchCounts


	def getSearchResults(self, searchID):
		sql = "SELECT pubID from searchpublink where searchID=%s;" % (searchID)
		self.cursor.execute(sql)
		results = self.cursor.fetchall()

		return results

	"""
	Returns a list of publication IDs that are mapped to both searchIDs in searchpublink
	"""
	def getOverlappingResults(self, searchID1, searchID2):

		results1 = self.getSearchResults(searchID1)

		results2 = self.getSearchResults(searchID2)

		results = []
		for r in results1:
			if r in results2:
				results.append(r)

		return results


	def shutdown(self):
		self.conn.commit()
		self.conn.close()
