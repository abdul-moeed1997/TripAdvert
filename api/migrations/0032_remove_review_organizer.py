# Generated by Django 3.0 on 2020-06-13 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_notification_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='organizer',
        ),
    ]
