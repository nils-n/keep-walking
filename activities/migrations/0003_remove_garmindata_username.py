# Generated by Django 3.2.20 on 2023-08-31 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_alter_garmindata_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='garmindata',
            name='username',
        ),
    ]