# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20160519_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='img',
            field=models.ImageField(null=True, upload_to=b'upload'),
        ),
    ]
