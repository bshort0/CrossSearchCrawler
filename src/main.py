from requests import session
from bs4 import BeautifulSoup
import sys


# Set up a global set of all search results
# Will be a set of three-tuples. (title, author, DOI)
results = set()

# Set up a dictionary for the program flags/options
flags = dict()

# Supported flags for fuzz
flags['searchTermsPath'] = ""


"""
Reads valid flags that were passed as arguments when running fuzz
"""
def parseFlags(options):
    for flag in options:
        # Ensure that the flag follows proper syntax
        if "--" in flag and "=" in flag:
            # Get the string from -- to = sign
            flagName = flag[(flag.find("--") + 2):flag.find("=")]
            # Get the string after the = sign
            flagValue = flag[(flag.find("=") + 1)::].lower()
            if flagName in flags:
                flags[flagName] = flagValue
            else:
                print("Unrecognized flag: " + flagName)
        else:
            print("Improper flag syntax: " + flag)


def main():
    if len(sys.argv) > 1:
        parseFlags(sys.argv[1::])
        searchTerms = parseSearchTermsFile(flags['searchTermsPath'])
	    searchMod = searchModuleIEEE(searchTerms, results)

    else:
        print("Incorrect number of arguments. Get help.\n")

if __name__ == "__main__":
	main()
