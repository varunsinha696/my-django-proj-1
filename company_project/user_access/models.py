from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    VIEWER = 'Viewer'
    MANAGER = 'Manager'
    AUDITOR = 'Auditor'

    ROLE_CHOICES = [
        (VIEWER, 'Viewer'),
        (MANAGER, 'Manager'),
        (AUDITOR, 'Auditor'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=VIEWER)

    def __str__(self):
        return self.username


class ProductMain(models.Model):
    product = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='manages')
    auditor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='audits')
    decommissioned = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name
