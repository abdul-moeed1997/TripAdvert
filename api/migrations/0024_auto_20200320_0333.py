# Generated by Django 3.0 on 2020-03-19 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20200320_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='api.Organizer'),
        ),
    ]