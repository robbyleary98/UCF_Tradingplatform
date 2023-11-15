from django.contrib import admin
from .models import Profile, Ticker, Portfolio, Transaction, StockData, Client


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'financial_goal', 'risk_tolerance', 'investment_preference']
    search_fields = ['user__username']


@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'sector']
    search_fields = ['symbol', 'name']


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticker', 'shares', 'average_buy_price']
    list_filter = ['user', 'ticker']
    search_fields = ['ticker__symbol']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticker', 'transaction_type', 'shares', 'price_per_share', 'transaction_time']
    list_filter = ['user', 'transaction_type', 'ticker']
    search_fields = ['ticker__symbol']


@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'price', 'pe_ratio', 'eps', 'dividend_yield', 'book_value', 'last_updated']
    search_fields = ['ticker__symbol']


admin.site.register(Client)
