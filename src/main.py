from requests import session
from bs4 import BeautifulSoup
import sys

def main():
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