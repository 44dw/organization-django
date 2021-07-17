from rest_framework import generics
from . import serializers
from .models import Department
# from rest_framework.permissions import IsAdminUser


class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class DepartmentDetails(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


# class DepartmentCreate(generics.CreateAPIView):
#     queryset = Department.objects.all()
#     serializer_class = serializers.DepartmentSerializer
#     permission_classes = [IsAdminUser]

