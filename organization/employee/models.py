from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models


def validate_day_of_birth(value):
    date_to_compare = date.today() - relativedelta(years=18)
    MaxValueValidator(limit_value=date_to_compare).compare(value, date_to_compare)


class Employee(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(validators=[validate_day_of_birth])
    phone_number = models.CharField(max_length=12, validators=[RegexValidator(regex=r'^\+?7?\d{10}$',
                                                                              message="Phone number must be entered in "
                                                                                      "the format: '+79379951689'.")])
    email = models.EmailField()
    employment_date = models.DateField(validators=[MaxValueValidator(limit_value=date.today())])
    dismissal_date = models.DateField(validators=[MaxValueValidator(limit_value=date.today())], null=True)
    position = models.CharField(max_length=50)
    salary = models.PositiveBigIntegerField()
    is_leader = models.BooleanField()
    department = models.ForeignKey('department.Department',
                                   # protecting Department from deleting if it has employees
                                   on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} {self.surname}, {self.position}"
