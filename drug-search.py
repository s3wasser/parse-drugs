import urllib2

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

# read html from main drug page
req = urllib2.Request('https://www.drugs.com/drug_information.html', headers=headers)
response = urllib2.urlopen(req)
druglst_html = response.read()

# making soup for main drug page
from bs4 import BeautifulSoup
soup = BeautifulSoup(druglst_html, 'html.parser')

# create dictionary with links to each letter of alphabet
alphadict = {}
first = 'a'
i = 0
for link in soup.select(".alpha-list a"):
	alphadict[chr(ord(first) + i)] = "https://www.drugs.com" + link.get('href')
	i = i+1

# html request to make soup
def make_soup(link):
	req = urllib2.Request(link, headers=headers)
	response = urllib2.urlopen(req)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	return soup

# prints links corresponsing to inputted drug
def find_drug(drug):
	drug = drug.lower()
	alphasoup = make_soup(alphadict[drug[0]])

	alphalst = [alphadict[drug[0]]]
	# remove repeated links (a1, b1, ... , z1)
	for div in alphasoup.find_all("div", class_='paging-list-wrap'):
		div.decompose()
	# find links for remaining pages for each letter (a2, a3, ... , a34)
	for link in alphasoup.select(".paging-list-index a"):
		alphalst.append("https://www.drugs.com" + link.get('href'))

	for link in alphalst:
		moresoup = make_soup(link)
		drugs = moresoup.select('a.doc-type')
		if (drug >= drugs[0].string.lower() and 
			drug <= drugs[len(drugs)-1].string.lower()):
			for link in drugs:
				if (drug == link.string.lower()):
					print link
			break;