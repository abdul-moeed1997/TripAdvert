# Generated by Django 3.0 on 2020-03-19 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_event_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='name',
            new_name='title',
        ),
    ]
