from django.db import models

class UsersData (models.Model):
    username = models.CharField(max_length=40, null=False)
    email = models.EmailField
    is_staff = models.BooleanField
