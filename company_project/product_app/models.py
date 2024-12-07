from django.db import models
from user_access.models import ProductMain, CustomUser
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class ProductInfo(models.Model):
    product = models.OneToOneField(ProductMain, on_delete=models.CASCADE)
    description = models.TextField()
    date_of_initiation = models.DateField()
    sso_implemented = models.BooleanField(default=True)
    decommissioned = models.BooleanField(default=False)

    def __str__(self):
        return self.product.product_name

class SSO(models.Model):
    product = models.OneToOneField(ProductMain, on_delete=models.CASCADE)
    sso_implemented = models.BooleanField(default=False)
    sso_date = models.DateField(null=True, blank=True)
    sso_description = models.TextField(null=True, blank=True)  # New field

    def __str__(self):
        return f"Product: {self.product.product}, Manager: {self.product.manager}, Auditor: {self.product.auditor}, Decommissioned: {self.product.decommissioned}, SSO Implemented: {self.sso_implemented}"

class MFA(models.Model):
    product = models.OneToOneField(ProductMain, on_delete=models.CASCADE)
    mfa_implemented = models.BooleanField(default=True)
    mfa_date = models.DateField(null=True, blank=True)
    mfa_description = models.TextField(null=True, blank=True)  # New field

    def __str__(self):
        return f"Product: {self.product.product}, Manager: {self.product.manager}, Auditor: {self.product.auditor}, Decommissioned: {self.product.decommissioned}, MFA Implemented: {self.mfa_implemented}"

# Temporary SSO table
class SSOTemp(models.Model):
    product = models.ForeignKey(ProductMain, on_delete=models.CASCADE, related_name='sso_temp')
    sso_implemented = models.BooleanField(default=False)
    sso_date = models.DateField(null=True, blank=True)
    sso_description = models.TextField(null=True, blank=True)  # New field
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='sso_updates')
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    remarks = models.TextField(null=True, blank=True)

# Temporary MFA table
class MFATemp(models.Model):
    product = models.ForeignKey(ProductMain, on_delete=models.CASCADE, related_name='mfa_temp')
    mfa_implemented = models.BooleanField(default=False)
    mfa_date = models.DateField(null=True, blank=True)
    mfa_description = models.TextField(null=True, blank=True)  # New field
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='mfa_updates')
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    remarks = models.TextField(null=True, blank=True)

# Notifications for updates
class Notification(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='sent_notifications')
    recipient = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='received_notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# Logs of updates
class Log(models.Model):
    requested_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='logs_requested')
    table_name = models.CharField(max_length=50)
    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='logs_reviewed')
    remarks = models.TextField(null=True, blank=True)
    date_of_modification = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('Approved', 'Approved'), ('Rejected', 'Rejected')])


class ProductInfoTemp(models.Model):
    product = models.ForeignKey(ProductMain, on_delete=models.CASCADE)
    description = models.TextField()
    date_of_initiation = models.DateField()
    sso_implemented = models.BooleanField(default=False)
    action_required = models.CharField(max_length=50, default='Pending')
    deleted_by_manager = models.BooleanField(default=False)

    def __str__(self):
        return f"Temp: {self.product.product}"
