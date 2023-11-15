"""
URL configuration for FA_FrontEnd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import FA_overview.views
import Registration.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', FA_overview.views.index, name='home'),
    path('login.html', Registration.views.login_user, name='login'),
    path('logout/', Registration.views.logout_user, name='logout'),
    path('register.html', Registration.views.register),
    path('stockdata/', FA_overview.views.fetch_stock_data, name='fetch_stock_data'),
    path('financial_data.html/', FA_overview.views.financial_data),
    path('bad_news.html/', FA_overview.views.fetch_bad_news)
]
