from bs4 import BeautifulSoup
import urllib
import csv
import pandas as pd

def read_page(hyperlink):
	fp = urllib.request.urlopen(hyperlink)
	mybytes = fp.read()
	mystr = mybytes.decode("utf8")
	fp.close()
	soup = BeautifulSoup(mystr, 'html.parser')
	return soup


if __name__ == "__main__":
	#Get base kialo page
	base_link = "https://www.kialo.com/"
	soup = read_page(base_link)

	#Iterate through topic pages and return html links for prompts
	debate_prompt_links = []
	for link in soup.find_all('a'):
		link_text = link.get('href')
		if 'tags' in link_text:
			topic_page_soup = read_page(link_text)
			for topic_page_link in topic_page_soup.find_all('a'):
				topic_page_link_text = topic_page_link.get('href')
				base_name = topic_page_link_text.split('/')[-1]
				base_name_split = base_name.split('-')
				if len(base_name_split) > 0:
					base_name_end = base_name_split[-1]
					if base_name_end.isnumeric():
						debate_prompt_links.append(topic_page_link_text)

	#Convert to csv
	df = pd.DataFrame(debate_prompt_links, columns=['links'])
	df.to_csv('links.csv', index=False)