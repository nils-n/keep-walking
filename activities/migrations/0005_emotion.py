# Generated by Django 3.2.20 on 2023-09-02 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0004_alter_garmindata_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[('0', 'BAD'), ('1', 'NEUTRAL'), ('2', 'GOOD'), ('3', 'UNDEFINED')], default='3')),
                ('created_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emotion_rating', to='activities.garmindata')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emotion_rating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
