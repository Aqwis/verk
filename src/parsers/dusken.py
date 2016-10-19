from bs4 import BeautifulSoup

def parse(raw_html, verbose=False):
	soup = BeautifulSoup(raw_html, 'html.parser')
	contents_list = soup.find_all("section", class_='article')

	if len(contents_list) > 1:
	    raise Exception()

	contents = contents_list[0]
	try:
	    contents.find(class_='factboxcontainer').decompose()
	except:
	    pass
	lines = list([s.replace('\n', ' ') for s in contents.stripped_strings])
	return " ".join(lines)