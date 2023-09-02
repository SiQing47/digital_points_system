import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_balance = models.IntegerField()
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=[
        ('increase', 'Increase'),
        ('decrease', 'Decrease')
    ])
    source = models.CharField(max_length=255)
    description = models.TextField()
    remaining_balance = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
