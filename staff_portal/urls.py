from django.urls import path 
from . views import * 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', StaffPortalLoginView.as_view(), name='staff-login'),
    path('register/', StaffRegistrationView.as_view(), name='staff-register'),
    path('dashboard/', dashboard, name='staff-dashboard'),
    path('logout/', staff_logout, name='staff-logout'),

]
