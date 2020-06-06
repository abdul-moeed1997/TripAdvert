# Generated by Django 3.0 on 2020-06-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_person_firebaseinstancetoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone_no',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
