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

# loop through first page of each letter in alphabet (a1, b1, ... , z1)
for link in soup.select(".alpha-list a"):
	# read html from first page of each letter in alphabet
	req = urllib2.Request("https://www.drugs.com" + link.get('href'), headers=headers)
	response = urllib2.urlopen(req)
	alpha = response.read()
	alphasoup = BeautifulSoup(alpha, 'html.parser')
	# find links for each drug on firts page
	for link in alphasoup.select("a.doc-type-pro"):
		print link.get('href')
	# remove repeated links (a1, b1, ... , z1)
	for div in alphasoup.find_all("div", class_='paging-list-wrap'):
		div.decompose()
	# find links for remaining pages for each letter (a2, a3, ... , a34)
	for link in alphasoup.select(".paging-list-index a"):
		req = urllib2.Request('https://www.drugs.com/drug_information.html', headers=headers)
		response = urllib2.urlopen(req)
		nextalpha = response.read()
		nextalphasoup = BeautifulSoup(nextalpha, 'html.parser')
		for link in nextalphasoup.select("a.doc-type-pro"):
			print link.get('href')


