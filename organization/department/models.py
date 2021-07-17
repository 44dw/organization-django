from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=25)
    creation_date = models.DateTimeField()

    def __str__(self):
        return self.name