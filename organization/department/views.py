from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Department, SalaryFund
from employee.models import Employee
# from rest_framework.permissions import IsAdminUser


class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class DepartmentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class DepartmentByName(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    lookup_field = 'name'


class SubordinateList(APIView):

    def is_show_all(self, params):
        if 'all' in params:
            return bool(params['all'])
        return False

    def get_strait_subordinates(self, department_id):
        return Department.objects.filter(parent_department_id=department_id)

    def get_all_subordinates(self, department_id, visited):
        subordinates = self.get_strait_subordinates(department_id)
        visited.extend(subordinates)
        for dep in subordinates:
            self.get_all_subordinates(dep.id, visited)
        return visited

    def get_subordinates(self, department_id, all_subordinates=False):
        if all_subordinates:
            return self.get_all_subordinates(department_id, [])
        return self.get_strait_subordinates(department_id)

    def get(self, request, pk):
        get_object_or_404(Department, pk=pk)
        show_all = self.is_show_all(request.GET)
        subordinates = self.get_subordinates(pk, show_all)
        return Response(serializers.DepartmentSerializer(subordinates, many=True).data)

class UpperList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer

    def collect_upper_departments(self, department, visited):
        if department is None:
            return visited
        visited.append(department)
        parent = department.parent_department
        return self.collect_upper_departments(parent, visited)

    def get_queryset(self):
        department_id = self.kwargs['pk']
        department = super().get_queryset().get(id=department_id)
        return self.collect_upper_departments(department.parent_department, [])


class RenameDepartment(APIView):

    def put(self, request, pk):
        new_department_name = request.query_params['name']
        if not new_department_name:
            return Response('name must be provided!', status=status.HTTP_400_BAD_REQUEST)
        department = get_object_or_404(Department, pk=pk)
        department.name = new_department_name
        serializer = serializers.DepartmentSerializer(department, data=model_to_dict(department))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoveDepartment(APIView):

    def put(self, request, pk, parent_department_id):
        department = get_object_or_404(Department, pk=pk)
        new_parent_department = get_object_or_404(Department, pk=parent_department_id)
        department.parent_department = new_parent_department
        serializer = serializers.DepartmentSerializer(department, data=model_to_dict(department))
        if serializer.is_valid():
            department.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentSalary(APIView):

    def get(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        employees = Employee.objects.filter(department_id=pk)
        pool_salary = sum(map(lambda e: e.salary, employees))
        return Response({"salary": pool_salary})


class DepartmentSalaries(generics.ListCreateAPIView):
    queryset = SalaryFund.objects.all()
    serializer_class = serializers.SalaryFundSerializer


class DepartmentSalaryDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = SalaryFund.objects.all()
    serializer_class = serializers.SalaryFundSerializer
