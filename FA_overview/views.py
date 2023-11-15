from django.http import HttpResponse
from django.shortcuts import render
from .financial_data import FinancialDataManager
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .bad_news_filter import BadNewsFilter
import pandas as pd
import os
import requests
import logging

def index(request):
    return render(request, "index.html")

@login_required
def fetch_stock_data(request):
    current_user = request.user.username
    excel_file_path = os.path.join(settings.BASE_DIR, 'FA_overview', 'Holdings.xlsx')
    df = pd.read_excel(excel_file_path)
    user_df = df[df['User'].str.lower() == current_user.lower()]

    if user_df.empty:
        return JsonResponse({'error': f'No holdings found for user {current_user}.'}, status=404)

    stock_symbols = user_df['Ticker'].dropna().tolist()
    data_manager = FinancialDataManager()
    stock_data = data_manager.fetch_stock_data(stock_symbols)

    combined_data = []

    if stock_data:
        for symbol in stock_symbols:
            shares_owned = user_df.loc[user_df['Ticker'] == symbol, 'Shares owned'].iloc[0]
            if pd.notnull(shares_owned):
                shares_owned = int(shares_owned)

            stock_info = stock_data.get(symbol.upper(), {})

            if 'error' not in stock_info:
                market_value = shares_owned * float(stock_info['Price'])

                combined_data.append({
                    'Ticker': symbol,
                    'Current Price': float(stock_info['Price']),
                    'Shares Owned': shares_owned,
                    'Market Value of Holdings': market_value,
                    'Dividend Yield': float(stock_info['Dividend_Yield']) if stock_info['Dividend_Yield'] else None,
                    'Shares Outstanding': int(stock_info['Shares_Outstanding']) if stock_info['Shares_Outstanding'] else None,
                    'EPS': float(stock_info['EPS']) if stock_info['EPS'] else None,
                    'Book_Value': 'N/A' if stock_info['Book_Value'] and float(stock_info['Book_Value']) < 0 else float(stock_info['Book_Value']) if stock_info['Book_Value'] else None,
                    'Adjusted_PB_Ratio': 'N/A' if stock_info['Adjusted_PB_Ratio'] is None else '{:.2f}'.format(float(stock_info['Adjusted_PB_Ratio'])) if float(stock_info['Adjusted_PB_Ratio']) >= 0 else 'N/A',
                })
            else:
                combined_data.append({
                    'Ticker': symbol,
                    'Current Price': 'Error fetching data',
                    'Shares Owned': shares_owned if pd.notnull(shares_owned) else None,
                    'Market Value of Holdings': 'N/A',
                    'Dividend Yield': 'N/A',
                    'Shares Outstanding': 'N/A',
                    'EPS': 'N/A',
                    'Book_Value': 'N/A',
                    'Adjusted_PB_Ratio': 'N/A'
                })

    sector_data = data_manager.fetch_sector_info(stock_symbols)

    sector_data_list = []

    if sector_data:
        for symbol in stock_symbols:
            sector_info = sector_data.get(symbol.upper(), {})

            if 'error' not in sector_info:
                sector_data_list.append({
                    'ShortName': sector_info.get('shortname', 'N/A'),
                    'Sector': sector_info.get('sector', 'N/A'),
                })
            else:
                sector_data_list.append({
                    'ShortName': sector_info.get('shortname', 'N/A'), 
                    'Sector': sector_info.get('sector', 'N/A'),
                })

    return JsonResponse({'stock_data': combined_data, 'sector_data': sector_data_list}, safe=False)

def financial_data(request):
    return render(request, "financial_data.html")

#Adding in
# @login_required
def fetch_bad_news(request):
    # Get the current logged-in user's username
    current_user = request.user.username

    # Construct the path to the Excel file using the BASE_DIR setting
    excel_file_path = os.path.join(settings.BASE_DIR, 'FA_overview', 'Holdings.xlsx')
    
    # Read the Excel file
    df = pd.read_excel(excel_file_path)
    
    # Filter the DataFrame for the current user
    user_df = df[df['User'].str.lower() == current_user.lower()]

    if user_df.empty:
        return JsonResponse({'error': f'No holdings found for user {current_user}.'}, status=404)

    # Convert the ticker symbols associated with the user into a list
    stock_symbols = user_df['Ticker'].dropna().tolist()

    # Create an instance of the BadNewsFilter
    news_filter = BadNewsFilter()

    # Initialize a dictionary to store bad news data for each stock symbol
    bad_news_data_dict = {}

    for symbol in stock_symbols:
        # Fetch bad news data for the current stock symbol
        bad_news_data = news_filter.fetch_bad_news([symbol])

        # Add the bad news data to the dictionary
        bad_news_data_dict[symbol] = bad_news_data

    return JsonResponse({'bad_news_data': bad_news_data_dict}, safe=False)