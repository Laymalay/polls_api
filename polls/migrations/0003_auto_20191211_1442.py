# Generated by Django 2.2.6 on 2019-12-11 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20191118_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='description',
            field=models.TextField(max_length=400, null=True),
        ),
    ]
