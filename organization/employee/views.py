from rest_framework import generics
from . import serializers
from .models import Employee
from department.models import Department
from django.shortcuts import get_object_or_404
from datetime import date
from django.utils.dateparse import parse_date
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView

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


class MoveAllToDepartment(APIView):

    def put(self, _, department_id, new_department_id):
        get_object_or_404(Department, pk=department_id)
        new_parent_department = get_object_or_404(Department, pk=new_department_id)
        department_employees = Employee.objects.filter(department_id=department_id)

        for e in department_employees:
            e.department = new_parent_department

        Employee.objects.bulk_update(department_employees, ['department'])
        serializer = serializers.EmployeeSerializer(department_employees, many=True)
        return Response(serializer.data)


class EmployeeSupervisor(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    def get_object(self):
        employee = super().get_object()

        if employee.is_leader:
            return employee

        department_employees = Employee.objects.filter(department_id=employee.department_id)
        return next((e for e in department_employees if e.is_leader), None)