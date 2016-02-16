from db import DBManager


"""
Called from the shell. Returns the count of publications returned for all of the given search IDs.
"""
def parseCountCommand(db, command):
	
	# split on whitespace and remove first value which should be "overlap"
	args = command.split()[1::]
	searchIDs = []
	for a in args:
		if a.isdigit():
			searchIDs.append(a)

	result = db.getOverlapIDs(searchIDs)
	print(len(result))


"""
Called from the shell. Prints publication info for the overlapping publications for the searchIDs to an output file.
"""
def parseSaveCountCommand(db, command):

	# split on whitespace and remove first command
	args = command.split()[1::]
	outputFile = args[0]
	args = args[1::]
	searchIDs = []
	for a in args:
		if a.isdigit():
			searchIDs.append(a)

	print("Writing results to: " + outputFile)

	results = db.getOverlapIDs(searchIDs)

	content = "Publication ID, Title, Year, DOI\n"
	for r in results:
		content += str(db.getPubById(r[0])) + "\n"

	with open(outputFile, 'w') as out:
		out.write(content)


"""
Called from the shell. Prints the search ids and their search text to the shell.
"""
def printSearchIDs(db):
	searches = db.getSearches()

	for s in searches:
		print(str(s[0]) + "|" + str(s[1]))


"""
Called from the shell. Saves the list of searches and IDs to a file.

Parameters:
	db: instance of DBManager
	command: the command entered into the shell. The first half is just the string that got this function called.
			The file path to print should be the second part of this string.
"""
def printSearchIDs(db, command):
	searches = db.getSearches()
	path = command.split()
	if len(path) > 1:
		path = path[1]
		content = "search ID | search Query text\n"
		for s in searches:
			content += str(s[0]) + "|" + str(s[1]) + "\n"

		with open(path, 'w') as out:
			out.write(content)
		print("Writing results to: " + path)

	else:
		content = "search ID | search Query text\n"
		for s in searches:
			content += str(s[0]) + "|" + str(s[1]) + "\n"
		print(content)
	

"""
Called from the shell. Prints out directions for using the shell.
"""
def help():
	print("None of the commands in the shell are case-sensitive. Use whatever you want.\n\n" + \
		  "To get out of the shell, you can use 'q', 'quit',  or 'exit'. Any of those will work.\n\n" + \
		  "To get the overlap of any number of searches, use 'count': \n\n" + \
		  "\t>count ID1 ID2 ... IDn\n\n" + \
		  "This command will get the number of publications that were returned for any combination of searches. The search ids in this command are separated by whitespace.\n\n" + \
		  "To get a list of the search query's IDs, just type 'search-ids' or 'ids'.\n" + \
		  "\t>search-ids\n\n" + \
		  "This will return a list of all of the ids mapped to their search query for all the saved searches in the database.\n\n" + \
		  "Don't want to have to print that every time to look up an id? Keep it handy by saving it to a file with 'save-searchids' or 'save-ids':\n" + \
		  "\t>save-ids /path/to/file\n\n" + \
		  "This command will take that same list printed by 'search-ids' and save it to a file for you to keep open for reference.\n\n" + \
		  "Want to see actual publication information from overlap queries instead of just the count? You're in luck! Use 'save-count'\n" + \
		  "\t>save-count /path/to/file ID1 ID2 ... IDn\n\n" + \
		  "This will find the overlap between any number of search IDs and print the publications id, title, year, and doi to the output file that you gave the path of.\n\n" + \
		  "Confused while in the shell? Type 'help' to get this same explanation right here!\n" + \
		  "\t>help\n\n"
		 )


"""
The main shell of the shell. Entry point for all of the commands. 

Parameters:
	db: A DBManager object

Returns:
	Nothing
"""
def run(db):

	print("Entering shell. See documentation or type 'help' for available commands.\nType \"quit\" or \"exit\" to leave.")
	command = input(">")
	while command.lower() != "quit" and command.lower() != "exit" and command.lower() != 'q':

		if command.lower().startswith("count"):
			parseCountCommand(db, command)

		elif command.lower().startswith("save-count"):
			parseSaveCountCommand(db, command)

		elif command.lower().startswith("searchids") or command.lower().startswith("ids"):
			printSearchIDs(db, command)

		elif command.lower().startswith("save-searchids") or command.lower().startswith("save-ids"):
			printSearchIDs(db, command)

		elif command.startswith("help"):
			help()

		else:
			print('"' + command + '" is not supported. See documentation or type help for supported commands.')
		command = input(">")


"""
Entry point of this file.

Just connects to the database and calls run
"""
def main():
	db = DBManager()

	run(db)

	
if __name__ == "__main__":
	main()