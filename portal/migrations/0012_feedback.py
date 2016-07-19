# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0011_auto_20160630_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ans1', models.CharField(max_length=100)),
                ('ans2', models.CharField(max_length=100)),
                ('ans3', models.CharField(max_length=100)),
                ('ans4', models.CharField(max_length=100)),
                ('ans5', models.CharField(max_length=100)),
                ('ans6', models.CharField(max_length=100)),
                ('admin', models.ForeignKey(related_name='admin_feedback', to='portal.MyUser', null=True)),
                ('client', models.ForeignKey(related_name='client_feedback', to='portal.MyUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
