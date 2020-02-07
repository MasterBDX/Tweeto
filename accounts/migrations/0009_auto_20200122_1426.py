# Generated by Django 3.0 on 2020-01-22 14:26

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200103_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.utils.get_proimage_name),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.utils.get_procover_name),
        ),
    ]