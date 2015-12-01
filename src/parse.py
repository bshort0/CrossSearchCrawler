
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


def reportToCSV(report):

    content = ""
    for line in report:
        for s in line:
            content += str(s) + ","
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
                contents.append(currentLine)
                currentLine = ""
            else:
                currentLine += char
        else:
            pass

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


def validateCSVfile(filePath):
	# Assumes that filePath has been checked to exist
	print("Cleaning CSV for: " + filePath)
	finalEntries = []
	header = getCSVHeader(filePath)
	finalEntries.append(header)
	entries = resultsFileToLists(filePath)
	finalEntries += entries

	contents = ""
	for entry in finalEntries:
		entry = validateCSVLine(entry)
		contents += entry + "\n"

	return contents


def compileFolder(filePaths):

	finalEntries = []

	header = parse.getCSVHeader(filePaths[0])
	finalEntries.append(header)
	for f in filePaths:
		entries = parse.resultsFileToLists(f)
		finalEntries += entries

	contents = parse.linesToCSV(finalEntries)

	return contents


def main():
	pass
	
if __name__ == "__main__":
	main()