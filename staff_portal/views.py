from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, JsonResponse
from hr.models import Employee
from core.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import redirect_to_login
import time
from core.utils import is_locked_out, send_sms
from django.utils import timezone

import random
LOCKOUT_PERIOD = 60 * 60  # 1 hour in seconds

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


class StaffRegistrationStep1View(View):
    template_name = 'core/auth/staff_register_step1.html'
    max_attempts = 3


    def get(self, request):
        # Reset attempts if expired or not set
        request.session['reg_attempts'] = 0
        return render(request, self.template_name, {'title': 'Staff Registration Step 1'})

    def post(self, request):
        staff_id = request.POST.get('staff_id')

        # Try to fetch employee early for DB-based lockout checks
        try:
            employee = Employee.objects.get(employee_id=staff_id)
        except Employee.DoesNotExist:
            # Fake a small delay to slow brute-force on invalid IDs
            import time as t
            t.sleep(1)
            return JsonResponse({
                "status": "fail",
                "message": "Invalid Staff ID."
            }, status=404)

        # Check for lockout
        if employee.reg_lockout_time:
            elapsed = (timezone.now() - employee.reg_lockout_time).total_seconds()
            if elapsed < LOCKOUT_PERIOD:
                mins_left = int((LOCKOUT_PERIOD - elapsed) // 60) + 1
                return JsonResponse({
                    "status": "fail",
                    "message": f"Too many failed attempts. You are locked out for {mins_left} more minute(s).", 
                    "next_url" : reverse('register-lockout')
                }, status=403)
            # Reset lockout if expired
            employee.reg_attempts = 0
            employee.reg_lockout_time = None
            employee.save()

        # Check if already registered
        if employee.user:
            return JsonResponse({
                "status": "fail",
                "message": "Account already registered. Please login or reset password."
            }, status=409)

        # Accept attempt
        if employee.reg_attempts >= self.max_attempts:
            employee.reg_lockout_time = timezone.now()
            employee.save()
            return JsonResponse({
                "status": "fail",
                "message": "Too many failed attempts. You are locked out for one hour.",
                "next_url": reverse('register-lockout')
            }, status=403)

        # If everything is okay, generate/send token
        token = random.randint(1000, 9999)
        request.session['reg_staff_id'] = staff_id
        request.session['reg_token'] = str(token)
        request.session['reg_phone'] = employee.phone_number

        # Send SMS
        sms_msg = f"Hi {staff_id}, Your staff portal registration code is {token}."
        response = send_sms(sms_msg, employee.phone_number)
        logging.info(f"SMS sent to {employee.phone_number} {token}: {response}")

        masked_phone = employee.phone_number[:3] + "xxxxx" + employee.phone_number[-2:]
        request.session['masked_phone'] = masked_phone

        # Reset attempts on success
        employee.reg_attempts = 0
        employee.reg_lockout_time = None
        employee.save()

        return JsonResponse({
            "status": "success",
            "message": f"Token sent to {masked_phone}",
            "next_url": "/staff-portal/register/verify/"
        })

def lockout_view(request):
    # Get employee and calculate seconds left as in your CBV
    lockout_seconds = 0  # Default
    staff_id = request.session.get('reg_staff_id')
    if staff_id:
        try:
            employee = Employee.objects.get(employee_id=staff_id)
            if employee.reg_lockout_time:
                elapsed = (timezone.now() - employee.reg_lockout_time).total_seconds()
                if elapsed < LOCKOUT_PERIOD:
                    lockout_seconds = int(LOCKOUT_PERIOD - elapsed)
        except Employee.DoesNotExist:
            pass
    return render(request, 'core/auth/register_lockout.html', {"lockout_seconds": lockout_seconds})
   

class StaffRegistrationStep2View(View):
    max_attempts = 3
    template_name = 'core/auth/staff_register_step2.html'
    
    def get(self, request):
        # redirect access to staff who wants to bypass step 1
        if not request.session.get('reg_staff_id'):
            return redirect('staff-register')
        
        context = {
            'title': 'Staff Registration Step 2',
            'masked_phone': request.session.get('masked_phone', '')
        }
        return render(request, self.template_name, context)


    def post(self, request):
        staff_id = request.session.get('reg_staff_id')
        if not staff_id:
            return JsonResponse({
                "status": "fail",
                "message": "Session expired. Please start registration again.",
                "next_url": reverse('staff-register')
            }, status=400)

        try:
            employee = Employee.objects.get(employee_id=staff_id)
        except Employee.DoesNotExist:
            return JsonResponse({
                "status": "fail",
                "message": "Session error. Please try again."
            }, status=400)

        # Check for lockout
        if employee.reg_lockout_time:
            elapsed = (timezone.now() - employee.reg_lockout_time).total_seconds()
            if elapsed < LOCKOUT_PERIOD:
                mins_left = int((LOCKOUT_PERIOD - elapsed) // 60) + 1
                return JsonResponse({
                    "status": "fail",
                    "message": f"Too many failed attempts. You are locked out for {mins_left} more minute(s).",
                    "next_url": reverse('register-lockout')
                }, status=403)
            # Reset lockout if expired
            employee.reg_attempts = 0
            employee.reg_lockout_time = None
            employee.save()

        token = request.POST.get('token')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        session_token = request.session.get('reg_token')

        # Use DB attempts for lockout, not session
        if employee.reg_attempts >= self.max_attempts:
            employee.reg_lockout_time = timezone.now()
            employee.save()
            return JsonResponse({
                "status": "fail",
                "message": "Too many failed attempts. You are locked out for one hour.",
                "next_url": reverse('register-lockout')
            }, status=403)

        # Validate token
        if token != session_token:
            employee.reg_attempts += 1
            if employee.reg_attempts >= self.max_attempts:
                employee.reg_lockout_time = timezone.now()
            employee.save()
            return JsonResponse({
                "status": "fail",
                "message": f"Incorrect token. Attempts left: {self.max_attempts - employee.reg_attempts}",
                "next_url": reverse('register-lockout') if employee.reg_attempts >= self.max_attempts else None
            }, status=401 if employee.reg_attempts < self.max_attempts else 403)

        # Validate passwords
        if password != password2:
            return JsonResponse({
                "status": "fail",
                "message": "Passwords do not match."
            }, status=400)

        # All good, create user, link, login
        user = CustomUser.objects.create_user(
            email=employee.email,
            password=password,
            first_name=employee.first_name,
            last_name=employee.last_name
        )
        employee.user = user
        employee.reg_attempts = 0
        employee.reg_lockout_time = None
        employee.save()

        # Clean up session
        for key in ['reg_token', 'reg_staff_id', 'reg_phone', 'masked_phone']:
            request.session.pop(key, None)

        login(request, user)
        return JsonResponse({
            "status": "success",
            "message": "Registration successful. Redirecting...",
            "redirect_url": "/staff-portal/dashboard/"
        })

