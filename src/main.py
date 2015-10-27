
import sys
from db import DBManager
from csv import DictReader
from os import listdir
from os.path import isfile, join

"""
Assumes that the input file is of proper format.
"""
def parseSearchResults(filePath):
    pass


def generateReport(dbManager):
    pass


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def parseCSVLine(line, headerNames):
    entry = {}
    i = 0
    currentItem = ""
    openQuote = False
    for char in line:
        if char == ',' and not openQuote:
            entry[headerNames[i]] = currentItem
            i += 1
            currentItem = ""
        elif char == '"' and not openQuote:
            openQuote = True
        elif char == '"' and openQuote:
            openQuote = False
        else:
            currentItem += char

    return entry

def parseFile(filePath):
    csvFile = open(filePath, encoding='utf-8').read()

    contents = []
    currentLine = ""
    for char in csvFile:
        if is_ascii(char):
            if char == "\n":
                currentLine += char
                contents.append(currentLine)
                currentLine = ""
            else:
                currentLine += char
        else:
            pass

    firstLine = contents[0]
    # Parse the first line to get the search query
    # 0 = url
    # 1 = date accessed
    # 2 = Search Query
    searchDetails = parseCSVLine(firstLine, ['url', 'date', 'query'])

    headerLine = contents[1]
    fieldNames = headerLine.replace('"', '').strip().split(',')

    contents = contents[2::]

    entries = []
    for line in contents:
        entry = parseCSVLine(line, fieldNames)
        entries.append(entry)

    return searchDetails, entries


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        # Should be path to a directory
        files = [ join(path, f) for f in listdir(path) if isfile(join(path, f)) ]

        for f in files:
            searchDetails, entries = parseFile(f)
            for row in entries:
                print(row)

        # FINALLY!!! Have parsed CSV. Now relate to search and put into database.

        db = DBManager()
        

    else:
        print("Incorrect arguments.")


if __name__ == "__main__":
	main()
