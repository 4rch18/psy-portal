# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('admin', models.ForeignKey(related_name='admin_time', to='portal.User')),
                ('client', models.ForeignKey(related_name='client_time', to='portal.User')),
                ('slot', models.ForeignKey(to='portal.TimeSlot')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='query',
            name='admin',
            field=models.ForeignKey(related_name='admin_text', to='portal.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='query',
            name='client',
            field=models.ForeignKey(related_name='client_text', to='portal.User'),
            preserve_default=True,
        ),
    ]
