# Generated by Django 3.2.20 on 2023-09-04 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='height_cm',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='step_goal',
        ),
    ]
