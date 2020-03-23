# Generated by Django 3.0 on 2020-03-23 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_delete_sessionlogin'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionLogin',
            fields=[
                ('session_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
