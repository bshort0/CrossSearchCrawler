
import sys
import os
from os.path import isfile, isfolder, join

from db import DBManager
import reports
import parse


def loadGoldenSet(db, taggedPath = "../zoteroExport/taggedPapers.csv", notApplicablePath = "../zoteroExport/notApplicable.csv"):

    if isfile(taggedPath):
        if isfile(notApplicablePath):
            tagSearchDetail, taggedEntries = parse.parseFile(taggedPath)
            naSearchDetail, naEntries = parse.parseFile(notApplicablePath)

            taggedEntries = parse.zoteroToIEEE(taggedEntries)
            naEntries = parse.zoteroToIEEE(naEntries)
            
            db.putSearchResults(tagSearchDetail, taggedEntries)
            db.putSearchResults(naSearchDetail, naEntries)
        else:
            pass
            # Print that the na path isn't there
    else:
        pass
        # print that the tagged path isn't there


def loadFolder(db, folderPath):

    if isfolder(folderPath):
        for root, dirs, files in os.walk(path):
            for f in files:
                loadFile(db, root + os.sep + f)
    else:
        pass


def loadFile(db, filePath):

    if isfile(filePath):
        print("Loading: " + f)
        searchDetails, entries = parse.parseFile(f)
        db.putSearchResults(searchDetails, entries)
    else:
        pass
        # Throw an error or something
    

def main():
    if len(sys.argv) > 1:

        db = DBManager()

        command = sys.argv[1]

        if command == "report-crossover":
            report = reports.generateReportCrossover(db)
            report = parse.reportToCSV(report)
            print(report)

        elif command == "report-by-year":
            report = reports.generateReportByYear(db)
            report = parse.reportToCSV(report)
            print(report)

        elif command == "report-by-authors":
            report = reports.generateAuthorReport(db)
            report = parse.reportToCSV(report)
            print(report)

        elif command == "compile-folder":

            path = sys.argv[2]
            outputFile = sys.argv[3]

            filePaths = []
            for root, dirs, files in os.walk(path):
                for f in files:
                    filePaths.append(root + os.sep + f)

            finalEntries = []
            header = parse.getCSVHeader(filePaths[0])
            finalEntries.append(header)
            for f in filePaths:
                entries = parse.resultsFileToLists(f)
                finalEntries += entries

            contents = parse.linesToCSV(finalEntries)

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
                print("Cleaning CSV for: " + f)
                finalEntries = []
                header = parse.getCSVHeader(f)
                finalEntries.append(header)
                entries = parse.resultsFileToLists(f)
                finalEntries += entries

                contents = ""
                for e in finalEntries:
                    contents += e + "\n"

                with open(f, 'w') as outFile:
                    outFile.write(contents)

        elif command == "load":

            path = sys.argv[2]
            # Should be path to a directory
            loadFolder(db, path)
            loadGoldenSet(db)


        else: 
            print("Incorrect arguments. Only 'report' and 'load' are currently supported.")
        
        db.shutdown()
        
    else:
        print("Incorrect arguments.")


if __name__ == "__main__":
	main()
