from django.urls import path 
from ..views import transaction_views as views
urlpatterns = [
     path('transactions/', views.index, name='transactions')
]
