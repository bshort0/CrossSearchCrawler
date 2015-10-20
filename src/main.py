from requests import session
from bs4 import BeautifulSoup
import sys

# Set up a dictionary for the program flags/options
flags = dict()

# Supported flags for fuzz
flags['custom-auth'] = ""
flags['common-words'] = ""
flags['vectors'] = ""
flags['sensitive'] = ""
flags['random'] = "false"
flags['slow'] = ".5"


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

	    pass

    else:
        print("Incorrect number of arguments. Get help.\n")

    # This is just a proof of concept that the acm can be searched programatically.
    with session() as s:
        response = s.get("http://dl.acm.org/advsearch.cfm?coll=DL&dl=ACM&CFID=553218618&CFTOKEN=75971898")
        # Get a beautiful soup object for this page
        soup = BeautifulSoup(response.text, "html.parser")
        print(soup.prettify().encode('utf8'))

        search = {"allofem" : '"Intrusion Detection System"'}
        response = s.get("http://dl.acm.org/advsearch.cfm?coll=DL&dl=ACM&CFID=553218618&CFTOKEN=75971898", params=search)
        soup = BeautifulSoup(response.text, "html.parser")
        print("\n\n\n====================\n\n")
        print(soup.prettify().encode('utf8'))

if __name__ == "__main__":
	main()
