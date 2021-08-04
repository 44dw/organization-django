from rest_framework import serializers
from .models import Department
from employee.models import Employee
from employee.serializers import EmployeeSerializer

def get_department_employees(dep_id):
    employees = Employee.objects.all()
    return list(filter(lambda e: e.department_id == dep_id, employees))


class DepartmentSerializer(serializers.ModelSerializer):
    department_leader = serializers.SerializerMethodField()
    employees_amount = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = '__all__'


    def get_department_leader(self, dep):
        department_employees = get_department_employees(dep.id)
        leader = next((e for e in department_employees), None)
        if leader:
            return EmployeeSerializer(leader).data

    def get_employees_amount(self, dep):
        department_employees = get_department_employees(dep.id)
        return len(department_employees)


    def validate_parent_department(self, value):

        def validate_parent_department_not_null(value, departments):
            is_root_department_exists = any(department.parent_department is None for department in departments)
            if is_root_department_exists and value is None:
                raise serializers.ValidationError('root department must be only one!')

        all_depts = Department.objects.all()
        validate_parent_department_not_null(value, all_depts)
        return value
