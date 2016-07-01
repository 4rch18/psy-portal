# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20160626_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='accepted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='slot',
            field=models.ForeignKey(related_name='slot_time', to='portal.TimeSlot'),
            preserve_default=True,
        ),
    ]
