from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    def validate_is_leader(self, value):

        def filter_by_department(employee, target_dep):
            employee_dep = employee.department
            if not employee_dep:
                return False
            is_target_dep = employee_dep.id == target_dep
            return all([is_target_dep, employee.is_leader])

        if value:
            data = self.get_initial()
            department = int(data['department'])
            employees = Employee.objects.all()
            filtered = list(filter(lambda e: filter_by_department(e, department), employees))
            department_has_leader = bool(filtered)
            if department_has_leader:
                raise serializers.ValidationError(f"department already has leader")
        return value

