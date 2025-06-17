from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, JsonResponse
from hr.models import Employee
from core.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import redirect_to_login


import logging
# Create your views here.

def staff_portal_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to staff portal login, not admin login!
            return redirect_to_login(request.get_full_path(), login_url='/staff-portal/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

class StaffPortalLoginView(View):
    template_name = "core/auth/staff_login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        staff_id = request.POST.get("staff_id")
        password = request.POST.get("password")

        try:
            employee = Employee.objects.get(employee_id=staff_id)
            if not employee.user:
                return JsonResponse({'status': 'fail', 'message': "Account not activated. Please register or contact HR."}, status=401)
            email = employee.email
            user = authenticate(request, email=email, password=password)
            if user is None:
                try:
                    CustomUser.objects.get(email=email)
                    return JsonResponse({'status': 'fail', 'message': "Sorry, email and password combination is incorrect"}, status=401)
                except CustomUser.DoesNotExist:
                    return JsonResponse({'status': 'fail', 'message': "Oops, user does not exist"}, status=404)
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next', '/staff-portal/dashboard/')
            return JsonResponse({'status': 'success', 'message': 'Login successful', 'redirect_url': next_url}, status=200)
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': "Oops, your record don't seem to exist, kindly contact HR admin"}, status=404)


def staff_logout(request):
    logout(request)
    return redirect('staff-login')  # or whatever your login URL name is

@staff_portal_login_required
def dashboard(request):
    return render(request, 'core/staff_dashboard.html')


class StaffRegistrationView(View):
    template_name = 'core/staff_register.html'
    max_attempts = 3
    lockout_minutes = 60

    