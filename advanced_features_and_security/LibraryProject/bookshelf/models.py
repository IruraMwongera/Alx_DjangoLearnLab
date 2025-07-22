# school/models.py

from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_view", "Can view subject"),
            ("can_create", "Can create subject"),
            ("can_edit", "Can edit subject"),
            ("can_delete", "Can delete subject"),
        ]

    def __str__(self):
        return self.name

