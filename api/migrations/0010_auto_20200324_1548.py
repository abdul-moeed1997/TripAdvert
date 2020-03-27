# Generated by Django 3.0 on 2020-03-24 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_person_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='comment',
        ),
        migrations.CreateModel(
            name='EventSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_description', models.CharField(blank=True, max_length=255)),
                ('detail_description', models.CharField(blank=True, max_length=255)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='api.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]