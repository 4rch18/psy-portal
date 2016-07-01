# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_auto_20160629_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='booked_by_username',
            field=models.CharField(default='zzz', max_length=40),
            preserve_default=False,
        ),
    ]
