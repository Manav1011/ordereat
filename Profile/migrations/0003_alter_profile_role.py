# Generated by Django 5.2.1 on 2025-06-07 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_alter_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('franchise_owner', 'Frachise Owner'), ('outlet_owner', 'Outlet Owner')], max_length=128),
        ),
    ]
