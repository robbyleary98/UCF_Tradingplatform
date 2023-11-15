import requests
import logging
import json

class BadNewsFilter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.headers = {
            "X-RapidAPI-Key": "54f6416fb1mshaed217b08778aeep12ff0djsn94c480b17b7c",
            "X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
        }
        # Make sure there's a comma after each keyword
        self.negative_keywords = [
            'crash', 'drop', 'plunge', 'down', 'decline', 'decrease', 'loss',
            'cut', 'bear', 'bad news', 'trouble', 'problem', 'issue', 'fall', 'dip',
            'hurdle'
        ]

    def fetch_bad_news(self, symbols):
        bad_news_results = {}
        for symbol in symbols:
            url = f"https://yahoo-finance127.p.rapidapi.com/news/{symbol.lower()}"
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                news_data = response.json()

                # Assuming news_data['articles'] is a list of articles
                news_articles = news_data.get('articles', [])

                # Initialize a list to store filtered articles
                filtered_articles = []

                for article in news_articles:
                    if 'title' in article:
                        title = article['title']
                        # Check if any negative keyword is present in the title
                        if any(keyword in title.lower() for keyword in self.negative_keywords):
                            filtered_articles.append({'title': title, 'link': article.get('link', '')})

                bad_news_results[symbol.upper()] = filtered_articles

            except requests.HTTPError as http_err:
                self.logger.error(f'HTTP error occurred for {symbol}: {http_err}')
                bad_news_results[symbol.upper()] = [{'error': str(http_err)}]
            except Exception as err:
                self.logger.error(f'Other error occurred for {symbol}: {err}')
                bad_news_results[symbol.upper()] = [{'error': str(err)}]

        return bad_news_results
