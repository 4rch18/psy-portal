# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20160626_1600'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User1',
            new_name='User',
        ),
    ]
