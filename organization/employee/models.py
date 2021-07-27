from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator
from datetime import date
from dateutil.relativedelta import relativedelta


def validate_day_of_birth(value):
    date_to_compare = date.today() - relativedelta(years=18)
    MaxValueValidator(limit_value=date_to_compare).compare(value, date_to_compare)


class Employee(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(validators=[validate_day_of_birth])
    phone_number = models.CharField(max_length=11, validators=[RegexValidator(regex=r'^\+?1?\d{10}$', message="Phone number must be entered in the format: '+79379951689'.")])
    email = models.EmailField()
    employment_date = models.DateField(validators=[MaxValueValidator(limit_value=date.today())])
    dismissal_date = models.DateField(validators=[MaxValueValidator(limit_value=date.today())], blank=True)
    position = models.CharField()
    salary = models.BigIntegerField()
    is_leader = models.BooleanField()

