# Generated by Django 4.1.6 on 2023-04-05 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content_type', models.CharField(choices=[('text/plain', 'Plain'), ('text/markdown', 'Markdown'), ('application/base64', 'Base64'), ('image/png;base64', 'Png'), ('image/jpeg;base64', 'Jpeg')], default='text/plain', max_length=200)),
                ('published', models.DateTimeField()),
                ('comment', models.TextField(max_length=301)),
                ('type', models.CharField(max_length=8)),
                ('id', models.CharField(max_length=250)),
                ('parent_comment_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.comments')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
