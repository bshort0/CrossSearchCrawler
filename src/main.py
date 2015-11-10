
import sys
import os
from db import DBManager
from csv import DictReader
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

    # Add on the last item
    entry[headerNames[i]] = currentItem
    i += 1

    while i < len(headerNames):
        entry[headerNames[i]] = ""
        i += 1

    return entry

def parseFile(filePath):
    csvFile = open(filePath, mode="r", errors="ignore").read()

    contents = []
    currentLine = ""
    for char in csvFile:
        if is_ascii(char):
            if char == "\n":
                contents.append(currentLine)
                currentLine = ""
            elif char == '\t':
                currentLine += ","
            else:
                currentLine += char
        else:
            pass

    firstLine = contents[0].strip().strip(',')
    searchDetails = parseCSVLine(firstLine, ['url', 'date', 'query', 'site'])

    headerLine = contents[1]
    fieldNames = headerLine.replace('"', '').strip().split(',')

    contents = contents[2::]

    entries = []
    for line in contents:
        entry = parseCSVLine(line, fieldNames)
        entries.append(entry)

    return searchDetails, entries

def zoteroToIEEE(zoteroEntries):

    transfers = {"Title" : "Document Title", "Author" : "Authors", "URL" : "PDF Link", "Publication Year" : "Year"}
    converted = []

    
    for entry in zoteroEntries:
        newEntry = {}
        for k in entry.keys():
            if k in transfers.keys():
                newEntry[transfers[k]] = entry[k]
            else:
                newEntry[k] = entry[k]
        converted.append(newEntry)

    return converted



def main():
    if len(sys.argv) > 1:

        db = DBManager()

        path = sys.argv[1]
        # Should be path to a directory
        filePaths = []
        for root, dirs, files in os.walk(path):
            for f in files:
                filePaths.append(root + os.sep + f)
                print(root + os.sep + f)

        
        taggedPath = "../zoteroExport/taggedPapers.CSV"
        notApplicablePath = "../zoteroExport/notApplicable.CSV"

        tagSearchDetail, taggedEntries = parseFile(taggedPath)
        naSearchDetail, naEntries = parseFile(notApplicablePath)

        taggedEntries = zoteroToIEEE(taggedEntries)
        naEntries = zoteroToIEEE(naEntries)
        
        db.putSearchResults(tagSearchDetail, taggedEntries)
        db.putSearchResults(naSearchDetail, naEntries)

        for f in filePaths:
            searchDetails, entries = parseFile(f)
            # print("Number of entries: " + str(len(entries)))
            db.putSearchResults(searchDetails, entries)

        searches = db.getSearches()

        for i in range(0, (len(searches)-1)):
            for j in range((i+1), len(searches)):
                results = db.getOverlappingResults(searches[i][0], searches[j][0])
                print("Number of searches from search %s: %i" % (searches[i][1], len(db.getSearchResults(searches[i][0]))))
                print("Number of searches from search %s: %i" % (searches[j][1], len(db.getSearchResults(searches[j][0]))))
                print("Overlap between search %s and search %s is: %i" % (searches[i][1], searches[j][1], len(results)))

        db.shutdown()
        

    else:
        print("Incorrect arguments.")


if __name__ == "__main__":
	main()
