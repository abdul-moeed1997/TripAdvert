# Generated by Django 3.0 on 2020-03-23 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200324_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='name',
        ),
        migrations.AddField(
            model_name='person',
            name='last_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]