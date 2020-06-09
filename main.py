from flask import Flask, jsonify
from decouple import config as config_decouple

from scraper import scrape_hacker_news
from jobs_scraper import scrape_all

app = Flask(__name__)

enviroment = config['development']

if config_decouple('PRODUCTION', default=False):
    enviroment = config['production']

app.config.from_object(enviroment)

@app.route('/hacker-news', methods=['GET'])
def get_news():
    news = scrape_hacker_news()
    return jsonify({'news': news})


@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = scrape_all()
    return jsonify({'jobs': jobs})


if __name__ == '__main__':
    app.run(debug=True)