from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Department
# from rest_framework.permissions import IsAdminUser


class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class DepartmentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class RenameDepartment(APIView):

    def put(self, request, department_id):
        new_department_name = request.data['name']
        if not new_department_name:
            return Response('name must be provided!', status=status.HTTP_400_BAD_REQUEST)
        department = get_object_or_404(Department, pk=department_id)
        department.name = new_department_name
        serializer = serializers.DepartmentSerializer(department, data=model_to_dict(department))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)