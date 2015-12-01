
import sys
import os
from os.path import isfile, isdir, join

from db import DBManager
import reports
import parse

"""
Utility function to get file paths for every
file in this directory and subdirectories.

Assumes that the path that is passed in is a
valid path to a directory.
"""
def getFilePaths(folderPath):
    filepaths = []
    for root, dirs, files in os.walk(folderPath):
            for f in files:
                filepaths.append(root + os.sep + f)

    return filepaths


"""
Loads the two files from the golden set of tagged 
papers and not applicable papers.

Paths to the two files are set as default parameters
so that they can be changed when called, if needed.
"""
def loadGoldenSet(db, taggedPath = "../zoteroExport/taggedPapers.csv", notApplicablePath = "../zoteroExport/notApplicable.csv"):

    # Ensure that each file exists
    if isfile(taggedPath):
        if isfile(notApplicablePath):
            tagSearchDetail, taggedEntries = parse.parseFile(taggedPath)
            naSearchDetail, naEntries = parse.parseFile(notApplicablePath)

            # Convert the CSV entries to have IEEE headers
            # Because they were exported from Zotero, some header names
            # are different
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


"""
Load a folder of csv files into the database.

Iterates on all of the files from the 'folderPath' directory
as well as files from subdirectories. For each file, calls the
function 'loadFile' on it.
"""
def loadFolder(db, folderPath):

    if isdir(folderPath):
        filepaths = getFilePaths(folderPath)
        for f in filepaths:
            loadFile(db, f)
    else:
        pass


"""
Loads a single file into the database.
"""
def loadFile(db, filePath):

    if isfile(filePath):
        print("Loading: " + filePath)
        searchDetails, entries = parse.parseFile(filePath)
        db.putSearchResults(searchDetails, entries)
    else:
        pass
        # Throw an error or something
    


"""
The command-line interface for the program.
"""
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
            if isdir(path):
                filePaths = getFilePaths(path)
            else:
                pass
                # throw error or something

            contents = ""
            if len(filePaths) > 0:
                contents = parse.compileFolder(filePaths)
            else:
                pass
                # throw error or something

            outFile = open(outputFile, 'w')
            outFile.write(contents)
            outFile.close()

        elif command == "validateCSV":
            # For a given directory path,
            # traverses through each file and ensures
            # that they each follow valid CSV format
            path = sys.argv[2]
            if isfile(path):
                # If a file path was given, only cleanse that file
                contents = parse.validateCSVfile(f)
                
                with open(f, 'w') as outFile:
                    outFile.write(contents)

            elif isdir(path):
                # If a directory path was given, traverse all the files
                filePaths = getFilePaths(path)
                for f in filePaths:
                    contents = parse.validateCSVfile(f)
                    
                    with open(f, 'w') as outFile:
                        outFile.write(contents)
            else:
                pass

        elif command == "load":
            # Loads an entire folder of CSV files and the golden set 
            # into the database

            path = sys.argv[2]
            loadFolder(db, path)
            loadGoldenSet(db)


        else: 
            print("Incorrect arguments. Only 'report' and 'load' are currently supported.")
        
        db.shutdown()
        
    else:
        print("Incorrect arguments.")


if __name__ == "__main__":
	main()
