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
	try:
		req = urllib2.Request(link, headers=headers)
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, err:
		return -1
	else:
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')
		return soup

# prints links corresponsing to inputted drug
def find_drug2(drug):
	drug = drug.lower()
	alphasoup = make_soup(alphadict[drug[0]])

	alphalst = [alphadict[drug[0]]]
	# remove repeated links (a1, b1, ... , z1)
	for div in alphasoup.find_all("div", class_='paging-list-wrap'):
		div.decompose()
	# find links for remaining pages for each letter (a2, a3, ... , a34)
	for link in alphasoup.select(".paging-list-index a"):
		alphalst.append("https://www.drugs.com" + link.get('href'))

	druglinks = []
	for link in alphalst:
		moresoup = make_soup(link)
		drugs = moresoup.select('a.doc-type')
		if (drug >= drugs[0].string.lower() and 
			drug <= drugs[len(drugs)-1].string.lower()):
			for link in drugs:
				if (drug == link.string.lower()):
					druglinks.append(link.get('href'))
			break;
	if not druglinks:
		return -1
	else:
		druglinks.sort()
		return 'https://www.drugs.com' + druglinks[0]


def find_drug1(drug):
	drugsoup = make_soup('https://www.drugs.com/' + drug.lower() + '.html')
	if (drugsoup == -1):
		return find_drug2(drug)
	else:
		return 'https://www.drugs.com/' + drug.lower() + '.html'

def get_interactions(link):
	if (link == -1):
		return False
	drug = make_soup(link)
	for item in drug.select('.nav-item'):
		if ('interactions' == item.string.lower()):
			int_link = 'https://www.drugs.com' + item.get('href')
	intsoup = make_soup(int_link)
	majors = intsoup.select('.int_3 a')
	majlnk = False
	for item in majors:
		if ('major' in item.string.lower()):
			major_link = 'https://www.drugs.com/drug-interactions/' + item.get('href')
			majlnk = True
	if (majlnk == False):
		return False
	else:
		interactsoup = make_soup(major_link)
		if (interactsoup == -1): 
			return False
		interactions = []
		for item in interactsoup.select('.int_3 a'):
			if ('drug-interactions' in item.get('href')):
				interactions.append(item.string)
		return interactions