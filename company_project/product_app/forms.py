from django import forms
from user_access.models import ProductMain
from .models import SSO, SSOTemp

class ProductInfoForm(forms.ModelForm):
    class Meta:
        model = ProductMain
        fields = ['product', 'manager', 'auditor', 'decommissioned']


class SSOForm(forms.ModelForm):
    class Meta:
        model = SSO
        fields = ['sso_implemented', 'sso_date', 'sso_description']  # Include description

class SSOTempForm(forms.ModelForm):
    class Meta:
        model = SSOTemp
        fields = ['sso_implemented', 'sso_date', 'sso_description']  # Include description
