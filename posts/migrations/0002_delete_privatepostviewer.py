# Generated by Django 4.1.6 on 2023-03-04 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PrivatePostViewer',
        ),
    ]
