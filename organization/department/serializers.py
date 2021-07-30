from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    def validate_parent_department(self, value):

        def validate_parent_department_not_null(value, departments):
            is_root_department_exists = any(department.parent_department is None for department in departments)
            if is_root_department_exists and value is None:
                raise serializers.ValidationError('root department must be only one!')

        all_depts = Department.objects.all()
        validate_parent_department_not_null(value, all_depts)
        return value
