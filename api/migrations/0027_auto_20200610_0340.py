# Generated by Django 3.0 on 2020-06-09 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20200607_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventschedule',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='api.Event'),
        ),
    ]
