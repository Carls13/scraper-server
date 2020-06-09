import requests
from bs4 import BeautifulSoup
import pprint


PAGES_TO_SCRAPE = 5
def scrape_hacker_news():
	hn = []
	for i in range(PAGES_TO_SCRAPE):
		res = requests.get(f"https://news.ycombinator.com/news?p={i}")
		soup = BeautifulSoup(res.text, 'html.parser')
		links = soup.select('.storylink')
		subtextes = soup.select('.subtext')
		hn.extend(create_custom_hn_page(links, subtextes))
	return sort_stories_by_votes(hn)

def sort_stories_by_votes(hnlist):
	return sorted(hnlist,  key= lambda k:k['votes'], reverse=True)

def create_custom_hn_page(links, subtextes):
	page = []
	for idx, item in enumerate(links):
		title = links[idx].getText()
		href = links[idx].get("href", None)
		vote = subtextes[idx].select('.score')
		if len(vote):
			points = int(vote[0].getText().replace(" points", ""))
			if points > 99:
				page.append({"title": title, "link": href, "votes": points})
	return page

# pprint.pprint(scrape_hacker_news())