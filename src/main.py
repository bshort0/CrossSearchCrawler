
import sys
import os
import csv
from db import DBManager
from csv import DictReader
from os.path import isfile, join




def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def parseCSVLine(line, headerNames):
    entry = {}
    i = 0
    currentItem = ""
    openQuoteCount = 0
    char = ""
    for count in range(0, len(line)):
        char = line[count]
        if i < len(headerNames):
            if char == ',' and openQuoteCount == 0:
                entry[headerNames[i]] = currentItem
                i += 1
                currentItem = ""
            elif char == '"' and openQuoteCount == 0:
                openQuoteCount += 1
            elif char == '"':
                openQuoteCount -= 1
            else:
                currentItem += char
        else:
            break

    # Add on the last item
    if char != ',' and i < len(headerNames):
        entry[headerNames[i]] = currentItem

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
        if not containsStopWords(entry):
            entries.append(entry)

    return searchDetails, entries


def containsStopWords(entry):
    stopWords = ['table of content', 'abstract', 'content', 'preface', 'front matter', \
                 'title page', 'program guide', 'program at a glance', 'list of papers', \
                 'technical program', 'author index', 'tutorial', 'conference program', \
                 'general session', 'front cover', 'keyword index', "- toc", "book of abstracts"]

    if 'Document Title' in entry:
        title = entry['Document Title'].lower().strip('[]')
    elif 'Title' in entry:
        title = entry['Title'].lower().strip('[]')
    else:
        title = ""

    for word in stopWords:
        if title.startswith(word) or title.endswith(word):
            return True

    return False

def zoteroToIEEE(zoteroEntries):

    transfers = {"Title" : "Document Title", "Author" : "Authors", "Url" : "PDF Link", "Publication Year" : "Year"}
    converted = []

    for entry in zoteroEntries:
        newEntry = {}
        for k in entry.keys():
            if k in transfers.keys():
                newEntry[transfers[k]] = entry[k]
            elif k == "Pages":
                if "-" in entry[k]:
                    newEntry["Start Page"] = entry[k].split("-")[0]
                    newEntry["End Page"] = entry[k].split("-")[1]
                else:
                    newEntry["Start Page"] = ""
                    newEntry["End Page"] = ""
            else:
                newEntry[k] = entry[k]
        converted.append(newEntry)

    return converted


def generateReport(db):
    
    listTable = []
    searches = db.getSearches()

    firstLine = ['Total', 'Total']
    for s in searches:
        firstLine.append(s[1])

    listTable.append(firstLine)

    secondLine = ['Total', '']
    for s in searches:
        secondLine.append(str(len(db.getSearchResults(s[0]))))

    listTable.append(secondLine)

    for s in searches:
        line = [s[1], str(len(db.getSearchResults(s[0])))]
        for other in searches:
            line.append(str(len(db.getOverlappingResults(s[0], other[0]))))
        listTable.append(line)

    return listTable


def reportToCSV(report):

    content = ""
    for line in report:
        for s in line:
            content += s + ","
        content += "\n"

    return content


def linesToCSV(report):

    content = ""
    for line in report:
        content += line + "\n"

    return content


def getCSVHeader(filePath):
    csvFile = open(filePath, mode="r", errors="ignore").read()

    lineCount = 0
    contents = []
    currentLine = ""
    for char in csvFile:
        if lineCount < 2:
            if is_ascii(char):
                if char == "\n":
                    contents.append(currentLine)
                    lineCount += 1
                    currentLine = ""
                elif char == '\t':
                    currentLine += ","
                else:
                    currentLine += char
        else:
            break

    header = contents[0].strip().strip(',') + "\n" + contents[1].replace('"', '').strip().strip(",")

    return header


def resultsFileToLists(filePath):
    csvFile = open(filePath, mode="r", errors="ignore").read()

    contents = []
    currentLine = ""
    for char in csvFile:
        if is_ascii(char):
            if char == "\n":
                currentLine = validateCSVLine(currentLine)
                contents.append(currentLine)
                currentLine = ""
            elif char == '\t':
                currentLine += ","
            else:
                currentLine += char
        else:
            pass

    # Remove the first two lines which should be the header
    contents = contents[2::]

    return contents


# Removes meaningless quotes to make sure the line matches CSV standard
def validateCSVLine(line):

    # Replace triple quotes with double quotes
    line = line.replace('\"\"\"', '\"\"')
    # Start with the first character
    newLine = line[0]

    if newLine == '"':
        quoteCount = 1
    else:
        quoteCount = 0

    for i in range(1, (len(line)-1)):
        char = line[i]
        lastChar = line[(i-1)]
        nextChar = line[(i+1)]        

        if char == '"':
            quoteCount += 1
            if nextChar == ',' and (quoteCount % 2) == 0:
                newLine += char
            elif lastChar == ',' and quoteCount == 1:
                newLine += char
        elif char == ',' and (quoteCount % 2) == 0:
            quoteCount = 0
            newLine += char
        else:
            newLine += char

    if line[(len(line)-1)] == '"' or line[(len(line)-1)] == ',':
        newLine += line[(len(line)-1)]

    return newLine

    
def main():
    if len(sys.argv) > 1:

        db = DBManager()

        command = sys.argv[1]

        if command == "report":
            report = generateReport(db)
            report = reportToCSV(report)
            print(report)

        elif command == "compile-folder":

            path = sys.argv[2]
            outputFile = sys.argv[3]

            filePaths = []
            for root, dirs, files in os.walk(path):
                for f in files:
                    filePaths.append(root + os.sep + f)

            finalEntries = []
            header = getCSVHeader(filePaths[0])
            finalEntries.append(header)
            for f in filePaths:
                entries = resultsFileToLists(f)
                finalEntries += entries

            contents = linesToCSV(finalEntries)

            outFile = open(outputFile, 'w')
            outFile.write(contents)
            outFile.close()

        elif command == "cleanse-CSV":
            """
            Goes through each file in the directory given,
            reads each CSV line and validates it, then 
            rewrites to the file.
            """
            path = sys.argv[2]

            filePaths = []
            for root, dirs, files in os.walk(path):
                for f in files:
                    filePaths.append(root + os.sep + f)

            for f in filePaths:
                print("Fixing: " + f)
                finalEntries = []
                header = getCSVHeader(f)
                finalEntries.append(header)
                entries = resultsFileToLists(f)
                finalEntries += entries

                contents = ""
                for e in finalEntries:
                    contents += e + "\n"

                with open(f, 'w') as outFile:
                    outFile.write(contents)



        elif command == "load":

            path = sys.argv[2]
            # Should be path to a directory
            filePaths = []
            for root, dirs, files in os.walk(path):
                for f in files:
                    filePaths.append(root + os.sep + f)

            taggedPath = "../zoteroExport/taggedPapers.CSV"
            notApplicablePath = "../zoteroExport/notApplicable.CSV"

            tagSearchDetail, taggedEntries = parseFile(taggedPath)
            naSearchDetail, naEntries = parseFile(notApplicablePath)

            taggedEntries = zoteroToIEEE(taggedEntries)
            naEntries = zoteroToIEEE(naEntries)
            
            db.putSearchResults(tagSearchDetail, taggedEntries)
            db.putSearchResults(naSearchDetail, naEntries)

            for f in filePaths:
                print("Parsing: " + f)
                searchDetails, entries = parseFile(f)
                db.putSearchResults(searchDetails, entries)

        else: 
            print("Incorrect arguments. Only 'report' and 'load' are currently supported.")
        
        db.shutdown()
        
    else:
        print("Incorrect arguments.")


if __name__ == "__main__":
	main()
