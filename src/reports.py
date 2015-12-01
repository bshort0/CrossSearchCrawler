
from db import DBManager

def generateReportCrossover(db):

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

def generateReportByYear(db):
    
    listTable = []

    years = {}
    searches = db.getSearchesByYear()
    keys = searches.keys()

    firstLine = ['Year']
    for s in keys:
        firstLine.append(s)
        for y in searches[s].keys():
            if y not in years:
                years[y] = []
            years[y].append(searches[s][y])

    listTable.append(firstLine)

    yearKeys = sorted(years.keys())

    for y in yearKeys:
        line = []
        line.append(y)
        for count in years[y]:
            line.append(count)
        listTable.append(line)

    return listTable


def generateAuthorReport(db):

    listTable = []

    numAuthors = len(db.getAuthors())
    searchCounts = db.getSearchesToAuthorCount()

    searches = searchCounts.keys()

    firstLine = ['Search', 'Total']
    secondLine = ['Num Authors', numAuthors]
    for s in searches:
        firstLine.append(s)
        secondLine.append(searchCounts[s])

    listTable.append(firstLine)
    listTable.append(secondLine)
    
    return listTable

def main():
	pass
	
if __name__ == "__main__":
	main()