from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# url patterns for functions in core.views
urlpatterns = [
    path('', views.index, name='login'),
    path('accounts/login/', views.index, name='login'),

    path('logout/', views.logout_user, name='logout'),
    path('change-password/', views.change_password, name='change-password'),
    path('profile/', views.user_profile, name='profile'),
    path('developers-disclaimer/', views.disclaimer, name='disclaimer'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('logger/', views.test_logging_view, name='logger'),


]

# auth related URLS for password resets  
urlpatterns += [
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='core/auth/password_reset_form.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/auth/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/auth/password_reset_complete.html'
    ), name='password_reset_complete'),
]
