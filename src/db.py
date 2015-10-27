
import sqlite3

class DBManager:
	def __init__(self, connection="searches.db"):
		self.conn = sqlite3.connect(connection)
		self.cursor = self.conn.cursor()

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

		searchID = putSearch(searchDetails)
		for entry in entries:
			entryID = self.putEntry(entry)
			self.putSearchLink(searchID, entryID)


	def putSearch(self, search):
		exists = False

		# Check if this search has been inserted yet
		idSql = "SELECT id FROM searches WHERE searchText=%s AND site=%s;" %(search['query'], search['site'])
		self.cursor.execute(idSql)
		results = self.cursor.fetchall()
		if len(results) > 0:
			exists = True

		# If it doesn't exist, insert it
		if not exists:
			sql = "INSERT INTO searches (searchText, site) VALUES ( %s, %s);" %(search['query'], search['site'])
			self.cursor.execute(sql)

		# Get the ID
		self.cursor.execute(idSql)
		idVal = self.cursor.fetchone()

		return idVal


	def putEntry(self, entry):
		pass


	def putSearchLink(self, searchID, entryID):
		pass