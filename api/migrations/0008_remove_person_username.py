# Generated by Django 3.0 on 2020-03-23 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200324_0056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='username',
        ),
    ]
