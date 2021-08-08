from rest_framework import generics
from . import serializers
from .models import Employee


class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class EmployeeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class DepartmentEmployees(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    def get_queryset(self):
        department_id = self.kwargs['department_id']
        return filter(lambda e: e.department_id == department_id, super().get_queryset())
