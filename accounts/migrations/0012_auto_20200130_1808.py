# Generated by Django 3.0 on 2020-01-30 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_userprofile_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='color',
            field=models.CharField(default='#FF0000', max_length=120),
        ),
    ]
