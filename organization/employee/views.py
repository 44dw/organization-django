from rest_framework import generics
from . import serializers
from .models import Employee


class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class EmployeeDetails(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer