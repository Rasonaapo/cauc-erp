from django.shortcuts import render
from django.http import HttpResponse

def students(request):
    return HttpResponse('Students view here...')