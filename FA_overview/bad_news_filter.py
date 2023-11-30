import logging
import requests
import json

# List of negative keywords
negative_keywords = [
        'crash', 'drop', 'plunge', 'down', 'decline', 'decrease', 'loss',
        'cut', 'bear', 'bad news', 'trouble', 'problem', 'issue', 'fall', 'dip',
        'hurdle', 'bearish', 'volatile', 'correction', 'Sell-off', 'underperform',
        'Slump', 'downside', 'weakness', 'Bear market', 'Risky', 'Uncertainty',
        'panic', 'pessimism', 'Reducing earnings', 'Negative sentiment', 'oversold',
        'bankruptcy', 'illegal', 'corrupt', 'layoffs', 'short', 'leveraged', 'strike',
        'unethical', 'crisis', 'fraud', 'controversy', 'boycott'
]

headers = {
    "X-RapidAPI-Key": "54f6416fb1mshaed217b08778aeep12ff0djsn94c480b17b7c",
    "X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
}


# A function to get news for a given symbol and filter bad news
def get_bad_news_for_symbol(symbol):
    url = f"https://yahoo-finance127.p.rapidapi.com/news/{symbol.lower()}"
    response = requests.get(url, headers=headers)
    bad_news_articles = []

    if response.status_code == 200:
        data = response.json()

        # Assuming the JSON data is a dictionary where each article has an integer key
        for key, article in data.items():
            if any(negative_word in article['title'].lower() for negative_word in negative_keywords):
                bad_news_articles.append((article['title'], article['link']))

    return bad_news_articles