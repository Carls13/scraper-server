from flask import Flask, jsonify, request

from scraper import scrape_hacker_news
from jobs_scraper import scrape_all

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/hacker-news', methods=['GET'])
def get_news():
    news = scrape_hacker_news()
    return jsonify({'news': news})


@app.route('/jobs', methods=['GET'])
def get_jobs():
	query = request.args.get('query')
	jobs = scrape_all(query)
	return jsonify({'jobs': jobs})


if __name__ == '__main__':
    app.run(debug=True)