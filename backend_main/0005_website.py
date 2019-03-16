# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
from .models import MAX_WEBSITE_LENGTH


class Migration(migrations.Migration):

    dependencies = [
        ('backend_main', 'backend_main_org'),  # no .py
    ]

    operations = [
        migrations.AddField(
            model_name='backend_main',
            name='website',
            field=models.CharField(max_length=MAX_WEBSITE_LENGTH),
        ),
    ]
