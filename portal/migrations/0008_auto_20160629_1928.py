# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_auto_20160629_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='client',
            field=models.ForeignKey(related_name='client_slot', default=None, to='portal.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='is_free',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='office_hours',
            field=models.ForeignKey(related_name='office_slot', to='portal.OfficeHour'),
            preserve_default=True,
        ),
    ]
