# Generated by Django 3.0.1 on 2020-02-20 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200220_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]