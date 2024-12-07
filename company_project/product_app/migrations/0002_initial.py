# Generated by Django 5.1.3 on 2024-11-28 07:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_app', '0001_initial'),
        ('user_access', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinfo',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_access.productmain'),
        ),
        migrations.AddField(
            model_name='productinfotemp',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_access.productmain'),
        ),
    ]