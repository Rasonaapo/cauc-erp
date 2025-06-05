from django.urls import path
from ..views import account_views as views

urlpatterns = [
    path('chart-of-accounts/', views.index, name='chart-of-accounts'),
]
