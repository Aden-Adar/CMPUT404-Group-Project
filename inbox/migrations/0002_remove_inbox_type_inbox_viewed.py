# Generated by Django 4.1.6 on 2023-03-05 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inbox', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inbox',
            name='type',
        ),
        migrations.AddField(
            model_name='inbox',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
