# Generated by Django 5.1.3 on 2024-11-30 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0002_initial'),
        ('user_access', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MFA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mfa_implemented', models.BooleanField(default=False)),
                ('mfa_date', models.DateField(blank=True, null=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_access.productmain')),
            ],
        ),
        migrations.CreateModel(
            name='SSO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sso_implemented', models.BooleanField(default=False)),
                ('sso_date', models.DateField(blank=True, null=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_access.productmain')),
            ],
        ),
    ]