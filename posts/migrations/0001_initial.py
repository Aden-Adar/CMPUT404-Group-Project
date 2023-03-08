# Generated by Django 4.1.6 on 2023-03-03 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'Public'), ('FRIENDS', 'Friends'), ('PRIVATE', 'Private')], default='PRIVATE', max_length=7)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.CharField(choices=[('text/plain', 'Plain'), ('text/markdown', 'Markdown'), ('application/base64', 'Base64'), ('image/png;base64', 'Png'), ('image/jpeg;base64', 'Jpeg')], default='text/plain', max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('content', models.TextField(max_length=300)),
                ('unlisted', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrivatePostViewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='posts.posts')),
                ('viewer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
