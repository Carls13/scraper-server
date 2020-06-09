import requests
from bs4 import BeautifulSoup
import pprint

query = "java"


def scrape_get_on_board():
    res = requests.get(f"https://www.getonbrd.com/jobs-{query}")
    soup = BeautifulSoup(res.text, 'html.parser')
    offers = soup.select('.gb-results-list__item')

    gb_jobs = []

    for idx, item in enumerate(offers):
        # Gets offer detail link
        link = item.get("href")

        # Gets main container
        info_container = offers[idx].select(
            ".gb-results-list__main .gb-results-list__info")[0]
        offer_details = info_container.select(".gb-results-list__title")[0]
        strong = offer_details.select("strong")[0]
        modality_container = offer_details.select(".color-hierarchy3")[0]

        # Gets job and modality
        job = strong.getText()
        modality = modality_container.getText()

        offer_origin_container = info_container.select(".size0")[0]
        author = offer_origin_container.getText()
        second_escape = author.find("\n", 2)

        spans = offer_origin_container.select("span")[1:]

        # Gets city if exists, if not, it's a remote job
        if len(spans) > 1:
            city = spans[0].getText()
            country = spans[2].getText()
            place = city + ", " + country
        else:
            place = "Remote"

        date_container = offers[idx].select(".gb-results-list__date")[0]
        date = date_container.getText()

        # Convert info into dict
        offer_overview = {
            "job": job,
            "author": author[1:second_escape],
            "modality": modality,
            "place": place,
            "link": link,
            "date": date[1:-1]
        }

        gb_jobs.append(offer_overview)
        if len(gb_jobs) == 20:
            break
    return gb_jobs


def scrape_remoteok():
    res = requests.get(f"https://remoteok.io/remote-{query}-jobs")
    soup = BeautifulSoup(res.text, 'html.parser')
    offers = soup.select('.job')[:20]

    remoteok_jobs = []

    for offer in offers:
        link = offer.select("a")[0].get("href")
        author = offer.select(".companyLink")[0].select("h3")[0].getText()
        job = offer.select("h2")[0].getText()
        date = offer.select(".time")[0].select("a")[0].getText()

        # Convert info into dict
        offer_overview = {
            "job": job,
            "modality": 'Full Time',
            "author": author,
            "place": 'Remote',
            "link": "https://remoteok.io" + link,
            "date": date
        }
        remoteok_jobs.append(offer_overview)
    return remoteok_jobs


def scrape_triple_byte():
    res = requests.get(f"https://triplebyte.com/jobs/t/{query}")
    soup = BeautifulSoup(res.text, 'html.parser')
    offers = soup.select('.job')[:20]

    triple_byte_jobs = []

    for offer in offers:
        first_div = offer.select("div")[1].select("div")[0]
        role_anchor = first_div.select("a")[0]
        link = role_anchor.get("href")
        job = role_anchor.getText()

        author_anchor = first_div.select('a')[1]
        author = author_anchor.getText()

        place = offer.select(".text-xs.text-right.whitespace-no-wrap")[0].select(".mr-4")[0].getText()

        # Convert info into dict
        offer_overview = {
            "job": job,
            "modality": 'Full Time',
            "author": author,
            "place": place,
            "link": "https://triplebyte.com" + link,
            "date": 'Now'}

        triple_byte_jobs.append(offer_overview)

    return triple_byte_jobs


def scrape_all():
    jobs = []
    jobs += scrape_get_on_board()
    jobs += scrape_remoteok()
    jobs += scrape_triple_byte()
    return jobs


# pprint.pprint(scrape_all())