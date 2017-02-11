# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dictionary_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('definition', models.TextField(blank=True)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(to='dictionary_app.Word')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='word',
            name='definition',
        ),
        migrations.RemoveField(
            model_name='word',
            name='title',
        ),
        migrations.AddField(
            model_name='language',
            name='views',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='word',
            name='name',
            field=models.CharField(default=0, unique=True, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='word',
            name='slug',
            field=models.SlugField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='word',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
