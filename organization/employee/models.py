from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, RegexValidator
from datetime import date
from dateutil.relativedelta import relativedelta


def validate_day_of_birth(value):
    date_to_compare = date.today() - relativedelta(years=18)
    MaxValueValidator(limit_value=date_to_compare).compare(value, date_to_compare)


def validate_is_leader(self, value):
    if value:
        data = self.get_initial()
        print(data)
        department = data.department
        print(department)
        department_has_leader = filter(lambda e: all([e.department == department, e.is_leader]), Employee.objects.all())
        if department_has_leader:
            raise ValidationError(f"department {department} already has leader")


class Employee(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(validators=[validate_day_of_birth])
    phone_number = models.CharField(max_length=11, validators=[RegexValidator(regex=r'^\+?1?\d{10}$',
                                                                              message="Phone number must be entered in "
                                                                                      "the format: '+79379951689'.")])
    email = models.EmailField()
    employment_date = models.DateField(validators=[MaxValueValidator(limit_value=date.today())])
    dismissal_date = models.DateField(validators=[MaxValueValidator(limit_value=date.today())], null=True)
    position = models.CharField(max_length=50)
    salary = models.BigIntegerField()
    is_leader = models.BooleanField(validators=[validate_is_leader])
    department = models.ForeignKey('department.Department',
                                   # protecting Department from deleting if it has employees
                                   on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} {self.surname}, {self.position}"
