from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    financial_goal = models.TextField(null=True, blank=True)
    risk_tolerance = models.CharField(max_length=100, null=True, blank=True)
    investment_preference = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Ticker(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.symbol


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    shares = models.DecimalField(max_digits=10, decimal_places=2)
    average_buy_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'ticker')

    def __str__(self):
        return f"{self.ticker.symbol} - {self.user.username}"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES)
    shares = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.ticker.symbol}"


class StockData(models.Model):
    ticker = models.OneToOneField(Ticker, on_delete=models.CASCADE, related_name='stock_data')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    eps = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dividend_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    book_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker.symbol
