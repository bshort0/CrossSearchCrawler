
import sqlite3

class DBManager:
	def __init__(self, connection="searches.db"):
		self.conn = sqlite3.connect(connection)
		self.cursor = self.conn.cursor()
		self.count = 0

		self.initializeTables()

	def initializeTables(self):
		tableCommands = ['''CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY, name text)''', \
						 '''CREATE TABLE IF NOT EXISTS publications (id INTEGER PRIMARY KEY, title text, year text, doi text, isbn text, issn text)''', \
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

		idSql = 'SELECT id FROM publications WHERE title="%s" AND year="%s" AND doi="%s" AND isbn="%s" AND issn="%s"' % (entry['Document Title'], entry['Year'], entry['DOI'], entry["ISBN"], entry["ISSN"])
		self.cursor.execute(idSql)
		results = self.cursor.fetchall()

		if len(results) > 0:
			print("Length of results checking if pub exists: " + str(len(results)))
			self.count += 1
			print("Number of exists: " + str(self.count))
			exists = True

		if not exists:
			sql = 'INSERT INTO publications (title, year, doi, isbn, issn) VALUES ("%s", "%s", "%s", "%s", "%s");' % (entry['Document Title'], entry['Year'], entry['DOI'], entry['ISBN'], entry['ISSN'])
			self.cursor.execute(sql)

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


	def getSearches(self):
		sql = "SELECT id, searchText from searches;"
		self.cursor.execute(sql)

		return self.cursor.fetchall()


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
