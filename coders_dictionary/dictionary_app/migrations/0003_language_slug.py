# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_app', '0002_auto_20170208_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='slug',
            field=models.SlugField(default=0),
            preserve_default=False,
        ),
    ]
