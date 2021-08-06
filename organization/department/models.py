from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError


def validate_name_not_exists(value):
    has_dep_with_name = bool(list(filter(lambda d: d.name == value, Department.objects.all())))
    if has_dep_with_name:
        raise ValidationError(f"Department with name {value} already exists!")


class Department(models.Model):
    name = models.CharField(max_length=25)
    creation_date = models.DateField(validators=[MaxValueValidator(limit_value=date.today())])
    parent_department = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name