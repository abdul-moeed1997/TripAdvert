# Generated by Django 3.0 on 2020-03-23 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_sessionlogin'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='name',
            field=models.CharField(default='<django.db.models.fields.CharField><django.db.models.fields.CharField>', max_length=100),
        ),
    ]
