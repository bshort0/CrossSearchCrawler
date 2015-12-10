

def parseOverlapCommand(db, command):
	pass



def parseCountCommand(db, command):
	pass



def help():
	print("Help")



def run(db):

	print("Entering shell. See documentation or type 'help' for available commands.\nType \"quit\" or \"exit\" to leave.)
	command = input(">")
	while command.lower() != "quit" and command.lower() != "exit":

		if command.startswith("overlap"):
			parseOverlapCommand(db, command)

		elif command.startswith("count"):
			parseCountCommand(db, command)

		elif command.startswith("help"):
			help()

		else:
			print('"' + command + '" is not supported. See documentation or type help for supported commands.')
		command = input(">")



def main():
	pass

	
if __name__ == "__main__":
	main()