# Generated by Django 5.1.3 on 2024-11-28 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date_of_initiation', models.DateField()),
                ('sso_implemented', models.BooleanField(default=False)),
                ('decommissioned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInfoTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('date_of_initiation', models.DateField()),
                ('sso_implemented', models.BooleanField(default=False)),
                ('action_required', models.CharField(default='Pending', max_length=50)),
                ('deleted_by_manager', models.BooleanField(default=False)),
            ],
        ),
    ]
