import requests
import logging


class FinancialDataManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch_stock_data(self, symbols):
        results = {}
        for symbol in symbols:
            url = f"https://yahoo-finance127.p.rapidapi.com/price/{symbol.lower()}"
            headers = {
                "X-RapidAPI-Key": "54f6416fb1mshaed217b08778aeep12ff0djsn94c480b17b7c",
                "X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
            }
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code

                data = response.json()
                price = data.get('regularMarketPrice', {}).get('raw', 0)
                book_value = data.get('bookValue', {}).get('raw', 0)

                # Calculate the P/B ratio and adjust it by dividing by 1.2
                adjusted_pb_ratio = (price / book_value if book_value else float('inf')) / 1.2

                results[symbol] = {
                    'Price': price,
                    'Dividend_Yield': data.get('dividendYield', {}).get('raw', 0),
                    'Shares_Outstanding': data.get('sharesOutstanding', {}).get('raw', 0),
                    'EPS': data.get('epsTrailingTwelveMonths', {}).get('raw', 0),
                    'Book_Value': book_value,
                    'Adjusted_PB_Ratio': adjusted_pb_ratio
                }
            except requests.exceptions.HTTPError as http_err:
                self.logger.error(f'HTTP error occurred for {symbol}: {http_err}')  # HTTP error
                results[symbol] = {'error': f'HTTP error occurred: {http_err}'}
            except Exception as err:
                self.logger.error(f'Other error occurred for {symbol}: {err}')  # Other errors
                results[symbol] = {'error': f'Other error occurred: {err}'}

        return results
    
    def fetch_sector_info(self, symbols):
        stock_sector_info = {}  # Define the dictionary to store sector information
        for symbol in symbols:
            url = f"https://yahoo-finance127.p.rapidapi.com/search/{symbol}"
            headers = {
                "X-RapidAPI-Key": "54f6416fb1mshaed217b08778aeep12ff0djsn94c480b17b7c",
                "X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
            }
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    quotes = data.get('quotes', [])
                    for quote in quotes:
                        if quote['symbol'] == symbol:
                            sector = quote.get('sectorDisp', 'Sector not found')
                            shortname = quote.get('shortname', 'Name not found')
                            stock_sector_info[symbol] = {'sector': sector, 'shortname': shortname}
                            break
                else:
                    stock_sector_info[symbol] = {'sector': 'Error fetching data', 'shortname': 'Error fetching data'}
            except Exception as err:
                # Handle exceptions (e.g., log the error)
                stock_sector_info[symbol] = {'sector': 'Error', 'shortname': 'Error'}

        return stock_sector_info