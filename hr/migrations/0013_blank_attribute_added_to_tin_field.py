# Generated by Django 5.1.1 on 2025-06-18 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0012_customuser_linked_to_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='tin',
            field=models.CharField(blank=True, max_length=24, null=True, unique=True, verbose_name='TIN No.'),
        ),
    ]
