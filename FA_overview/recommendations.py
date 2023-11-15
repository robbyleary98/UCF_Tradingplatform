def get_sector_exposure_and_recommendations(user_id):
    raw_data = fetch_portfolio_data(user_id)

    # Convert raw data to list of Stock objects
    stocks = [Stock(*row) for row in raw_data]

    # Initialize sector exposure dictionary
    sector_exposure = {}
    sector_threshold = 0.02  # Minimum 2% allocation per sector
    max_sector_allocation = 0.75  # Maximum 75% allocation per sector

    # Calculate total investment
    total_investment = sum(stock.calculate_investment() for stock in stocks)

    # Update sector exposure
    for stock in stocks:
        investment = stock.calculate_investment()
        sector_exposure.setdefault(stock.sector, 0)
        sector_exposure[stock.sector] += investment

    # Prepare recommendations
    recommendations = []
    for sector, exposure in sector_exposure.items():
        sector_data = {
            'sector': sector,
            'exposure': exposure,
            'recommendation': '',
            'stocks': []
        }

        target_allocation = total_investment * sector_threshold
        if exposure < target_allocation:
            sector_data['recommendation'] = "Add more stocks in the sector to meet the 2% threshold."
        elif exposure > total_investment * max_sector_allocation:
            sector_data['recommendation'] = "Reduce exposure to the sector to stay below the 75% limit."
        else:
            sector_data['recommendation'] = "Portfolio allocation within desired limits."

        sector_stocks = [stock for stock in stocks if stock.sector == sector]
        sector_stocks.sort(key=lambda x: (-x.nwc, -x.dividend_yield, x.morningstar_ranking))

        for recommended_stock in sector_stocks:
            sector_data['stocks'].append({
                'ticker': recommended_stock.ticker,
                'nwc': recommended_stock.nwc,
                'dividend_yield': recommended_stock.dividend_yield,
                'morningstar_ranking': recommended_stock.morningstar_ranking
            })

        recommendations.append(sector_data)

    return {
        'total_investment': total_investment,
        'sector_exposure': sector_exposure,
        'recommendations': recommendations
    }
