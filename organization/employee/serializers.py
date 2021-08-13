from rest_framework import serializers
from .models import Employee


def find_department_leader(data):
    department_id = int(data['department'])
    employees = list(Employee.objects.filter(department_id=department_id))
    return next((e for e in employees if e.is_leader), None)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    def validate_salary(self, value):
        data = self.get_initial()
        if bool(data['is_leader']):
            return value
        leader = find_department_leader(data)
        if not leader or value < leader.salary:
            return value
        raise serializers.ValidationError('salary must not be higher then employees\'s leader\'s')

    def validate_is_leader(self, value):
        if value:
            data = self.get_initial()
            if find_department_leader(data):
                raise serializers.ValidationError('department already has leader')
        return value

