

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('sector', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')], max_length=4)),
                ('shares', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_per_share', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_time', models.DateTimeField(auto_now_add=True)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FA_overview.ticker')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pe_ratio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('eps', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dividend_yield', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('book_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('ticker', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stock_data', to='FA_overview.ticker')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('financial_goal', models.TextField(blank=True, null=True)),
                ('risk_tolerance', models.CharField(blank=True, max_length=100, null=True)),
                ('investment_preference', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shares', models.DecimalField(decimal_places=2, max_digits=10)),
                ('average_buy_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FA_overview.ticker')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'ticker')},
            },
        ),
    ]
