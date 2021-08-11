from rest_framework import generics
from . import serializers
from .models import Employee
from department.models import Department
from django.shortcuts import get_object_or_404
from datetime import date
from django.utils.dateparse import parse_date
from django.forms.models import model_to_dict
from rest_framework.response import Response

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


class Dismiss(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    def update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        data = request.data
        dismissal_date = parse_date(data['date']) if 'date' in data else date.today()
        employee = get_object_or_404(Employee, pk=pk)
        employee.dismissal_date = dismissal_date
        result = model_to_dict(employee)
        serializer = serializers.EmployeeSerializer(employee, data=result)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MoveToDepartment(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    def update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        new_department_id = kwargs['department_id']
        employee = get_object_or_404(Employee, pk=pk)
        new_department = get_object_or_404(Department, pk=new_department_id)
        if employee.department_id != new_department_id:
            employee.department = new_department
        result = model_to_dict(employee)
        serializer = serializers.EmployeeSerializer(employee, data=result)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
