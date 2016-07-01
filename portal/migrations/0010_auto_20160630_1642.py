# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_auto_20160629_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status_appointment_changed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_office_hours',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='updated_time_slots',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
