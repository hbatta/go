# Generated by Django 2.0.5 on 2018-05-23 23:29

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=100, verbose_name='verbose name')),
                ('organization', models.CharField(default='', max_length=100, verbose_name='verbose name')),
                ('description', models.TextField(blank=True, default='', verbose_name='verbose name')),
                ('registered', models.BooleanField(default=False, verbose_name='verbose name')),
                ('approved', models.BooleanField(default=False, verbose_name='verbose name')),
                ('blocked', models.BooleanField(default=False, verbose_name='verbose name')),
                ('user', models.OneToOneField(on_delete='cascade', to=settings.AUTH_USER_MODEL, verbose_name='Django User Object')),
            ],
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='verbose name')),
                ('date_expires', models.DateTimeField(blank=True, null=True, verbose_name='verbose name')),
                ('destination', models.URLField(default='https://go.gmu.edu', max_length=1000)),
                ('short', models.SlugField(max_length=20, unique=True)),
                ('clicks', models.IntegerField(default=0)),
                ('qrclicks', models.IntegerField(default=0)),
                ('socialclicks', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete='cascade', to='go.RegisteredUser', verbose_name='verbose name')),
            ],
            options={
                'ordering': ['short'],
            },
        ),
    ]