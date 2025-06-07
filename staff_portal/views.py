from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, JsonResponse
from hr.models import Employee
from core.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate

import logging
# Create your views here.
@never_cache
def index(request):

    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        # check Employee if ID exists
        try:
            employee = Employee.objects.get(employee_id=staff_id)
            email = employee.email
            password = request.POST.get('password')

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            if user is None:
                try:
                    # If user is None, check if the user exists for a better error message
                    CustomUser.objects.get(email=email)
                    return JsonResponse({'status': 'fail', 'message': "Sorry, email and password combination is incorrect"}, status=401)

                except CustomUser.DoesNotExist:
                    return JsonResponse({'status': 'fail', 'message': "Oops, user does not exist"}, status=200)
            
            # Log the user in if authentication is successful
            login(request, user)  

            next_url = request.POST.get('next') or request.GET.get('next', '/dashboard/')
    
            return JsonResponse({'status': 'success', 'message': 'Login successful', 'redirect_url':next_url}, status=200)

        except Employee.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': "Oops, your record don't seem to exist, kindly contact HR admin"}, status=200)
  

    return render(request, 'core/portal_login.html')