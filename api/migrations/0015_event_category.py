# Generated by Django 3.0 on 2020-03-19 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20200319_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.CharField(max_length=20, null=True),
        ),
    ]