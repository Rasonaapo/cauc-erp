from django.urls import path, include 

urlpatterns = [
    path('chart-of-accounts/', include('finance.urls.account_urls')),
    path('transactions/', include('finance.urls.transaction_urls')),
    path('operations/', include('finance.urls.operations_urls')),
]
# This file is used to include all the finance URLs in the main project URL configuration.
# It imports the necessary modules and defines the URL patterns for the finance app.
# Each URL pattern includes a specific module for handling different aspects of finance, such as accounts, transactions, and operations.
# This modular approach helps in organizing the code and makes it easier to maintain and extend in the future.