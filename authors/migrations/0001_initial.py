# Generated by Django 4.1.6 on 2023-04-05 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('github', models.CharField(blank=True, default='', max_length=200)),
                ('profileImage', models.TextField(blank=True, default='https://cdn0.iconfinder.com/data/icons/google-material-design-3-0/48/ic_account_circle_48px-512.png', max_length=10000, null=True)),
                ('password', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=6)),
                ('host', models.CharField(max_length=250)),
                ('url', models.CharField(max_length=250)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FollowingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=6)),
                ('summary', models.CharField(max_length=150)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor', to=settings.AUTH_USER_MODEL)),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_following', models.DateTimeField(auto_now_add=True)),
                ('following_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-started_following'],
            },
        ),
        migrations.AddConstraint(
            model_name='followingrequest',
            constraint=models.CheckConstraint(check=models.Q(('actor__isnull', False), ('object__isnull', False)), name='actor_and_object_not_null'),
        ),
        migrations.AddConstraint(
            model_name='following',
            constraint=models.CheckConstraint(check=models.Q(('user__isnull', False), ('following_user__isnull', False)), name='user_and_following_user_not_null'),
        ),
    ]
