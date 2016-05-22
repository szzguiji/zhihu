# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='city',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AddField(
            model_name='newuser',
            name='job',
            field=models.CharField(default=b'', max_length=20),
        ),
    ]
