# Generated by Django 3.0 on 2020-03-24 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20200324_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventschedule',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='api.Event'),
        ),
    ]
