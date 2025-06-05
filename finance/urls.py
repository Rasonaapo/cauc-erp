from django.urls import path, include 

urlpatterns = [
    path('chart-of-accounts/', include('finance.urls.account_urls')),
    path('transactions/', include('finance.urls.transaction_urls')),
    path('operations/', include('finance.urls.operations_urls')),
]
