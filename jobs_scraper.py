import requests
from bs4 import BeautifulSoup
import pprint
from datetime import date as dt, timedelta


def monthToNum(shortMonth):
    return {
            'Jan' : 1,
            'Feb' : 2,
            'Mar' : 3,
            'Apr' : 4,
            'May' : 5,
            'Jun' : 6,
            'Jul' : 7,
            'Aug' : 8,
            'Sep' : 9, 
            'Oct' : 10,
            'Nov' : 11,
            'Dec' : 12
    }[shortMonth]


def format_gb_date(date):
    month, day = date.split(" ")
    today = dt.today()
    year = today.year
    new_date = dt(year, monthToNum(month), int(day))
    if new_date > today:
        new_date = new_date - timedelta(days=365)
    return new_date.isoformat()


def format_remoteok_date(date):
    months = ['h', 'd', 'mo',  'yr']
    for month in months:
        if month in date:
            amount_before, other = date.split(month)
            m_start = date.find(month)
            unit = date[m_start:]
            break
    # Decide timedelta
    if unit == "h":
        delta = timedelta(hours=int(amount_before))
    if unit == "d":
        delta = timedelta(days=int(amount_before))
    if unit == "mo":
        delta = timedelta(days=30 * int(amount_before))
    if unit == "yr":
        delta = timedelta(days=365 * int(amount_before))

    final_date = dt.today() - delta
    return final_date.isoformat()


def get_triple_byte_date(i):
    today = dt.today()
    delta = timedelta(days=i)
    final_date = today - delta
    return final_date.isoformat()


def scrape_get_on_board(query):
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
        date = date_container.getText()[1:-1]

        # Convert info into dict
        offer_overview = {
            "job": job,
            "author": author[1:second_escape],
            "modality": modality,
            "place": place,
            "link": link,
            "date": format_gb_date(date)
        }

        gb_jobs.append(offer_overview)
        if len(gb_jobs) == 20:
            break
    return gb_jobs


def scrape_remoteok(query):
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
            "date": format_remoteok_date(date)
        }
        remoteok_jobs.append(offer_overview)
    return remoteok_jobs


def scrape_triple_byte(query):
    res = requests.get(f"https://triplebyte.com/jobs/t/{query}")
    soup = BeautifulSoup(res.text, 'html.parser')
    offers = soup.select('.job')[:20]

    triple_byte_jobs = []
    i = 0
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
            "date": get_triple_byte_date(i)}

        triple_byte_jobs.append(offer_overview)
        i += 1

    return triple_byte_jobs


def scrape_all(query):
    jobs = []
    jobs += scrape_get_on_board(query)
    jobs += scrape_remoteok(query)
    jobs += scrape_triple_byte(query)
    jobs = sorted(jobs,  key= lambda k:k['date'], reverse=True)
    return jobs