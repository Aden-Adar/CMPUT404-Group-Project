# Generated by Django 4.1.6 on 2023-02-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='comment_id',
        ),
        migrations.AddField(
            model_name='comments',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comments',
            name='content_type',
            field=models.CharField(choices=[('text/plain', 'Plain'), ('text/markdown', 'Markdown'), ('application/base64', 'Base64'), ('image/png;base64', 'Png'), ('image/jpeg;base64', 'Jpeg')], default='text/plain', max_length=200),
        ),
    ]
