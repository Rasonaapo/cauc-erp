from django.urls import path 
from ..views import operations_views as views 

urlpatterns = [
     path('students/', views.students, name='students'),
]
