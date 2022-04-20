from django.shortcuts import render
from .serializers import EmployeeSerializer
from .models import Employee
from rest_framework import viewsets
# Create your views here.


def main_page(request):
    return render(request, 'base/base.html')
