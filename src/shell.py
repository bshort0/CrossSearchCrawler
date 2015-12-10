from db import DBManager

def parseCountCommand(db, command):
	
	# split on whitespace and remove first value which should be "overlap"
	args = command.split()[1::]
	searchIDs = []
	for a in args:
		if a.isdigit():
			searchIDs.append(a)

	result = db.getOverlapIDs(searchIDs)
	print(len(result))



def parseOverlapCommand(db, command):

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


def help():
	print("Help")



def run(db):

	print("Entering shell. See documentation or type 'help' for available commands.\nType \"quit\" or \"exit\" to leave.")
	command = input(">")
	while command.lower() != "quit" and command.lower() != "exit" and command.lower() != 'q':

		if command.lower().startswith("count"):
			parseCountCommand(db, command)

		elif command.lower().startswith("print-overlap"):
			parseOverlapCommand(db, command)

		elif command.startswith("help"):
			help()

		else:
			print('"' + command + '" is not supported. See documentation or type help for supported commands.')
		command = input(">")



def main():
	db = DBManager()

	run(db)

	
if __name__ == "__main__":
	main()