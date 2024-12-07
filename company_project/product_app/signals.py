from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from user_access.models import ProductMain
from .models import SSO, MFA

# Handle changes to ProductInfo
@receiver(post_save, sender=ProductMain)
def sync_product_to_sso_and_mfa(sender, instance, created, **kwargs):
    if created:
        # When a new ProductInfo is created, create corresponding rows in SSO and MFA
        SSO.objects.create(product=instance)
        MFA.objects.create(product=instance)
    else:
        # When a ProductInfo is updated, ensure related tables reflect changes
        sso = SSO.objects.filter(product=instance).first()
        mfa = MFA.objects.filter(product=instance).first()
        
        if sso:
            sso.product = instance
            sso.save()
        
        if mfa:
            mfa.product = instance
            mfa.save()

@receiver(post_delete, sender=ProductMain)
def delete_product_related_data(sender, instance, **kwargs):
    # When a ProductInfo is deleted, delete related rows in SSO and MFA
    SSO.objects.filter(product=instance).delete()
    MFA.objects.filter(product=instance).delete()
