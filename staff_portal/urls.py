from django.urls import path 
from . views import * 
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('', StaffPortalLoginView.as_view(), name='staff-login'),
    path('register/', StaffRegistrationStep1View.as_view(), name='staff-register'),
    path('register/verify/', StaffRegistrationStep2View.as_view(), name='staff-register-step2'),
    path('lockout/', lockout_view, name='register-lockout'),

    path('dashboard/', dashboard, name='staff-dashboard'),
    path('logout/', staff_logout, name='staff-logout'),
    path('profile/', staff_profile, name='staff-profile'),
    path('profile/change-password/', staff_change_password, name='staff-change-password'),
    # path('profile/update/', staff_profile_update, name='staff-profile-update'),


]
