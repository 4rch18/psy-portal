# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_timeslot_booked_by_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeslot',
            old_name='is_booked',
            new_name='is_free',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='accepted',
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='booked_by_username',
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(default=b'pending', max_length=20),
            preserve_default=True,
        ),
    ]
