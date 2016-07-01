# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_auto_20160629_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='client',
            field=models.ForeignKey(related_name='client_slot', to='portal.User', null=True),
            preserve_default=True,
        ),
    ]
