# Generated by Django 3.0 on 2020-03-23 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_person_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
