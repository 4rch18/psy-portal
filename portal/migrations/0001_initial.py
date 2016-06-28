# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeHour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.CharField(max_length=10)),
                ('end_time', models.CharField(max_length=10)),
                ('display', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('text', models.CharField(max_length=200)),
                ('by_admin', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_booked', models.BooleanField(default=False)),
                ('display', models.CharField(max_length=40)),
                ('office_hours', models.ForeignKey(to='portal.OfficeHour')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('is_admin', models.BooleanField(default=False)),
                ('sent_new_text', models.BooleanField(default=False)),
                ('is_online', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='query',
            name='admin',
            field=models.ForeignKey(related_name='admin', to='portal.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='query',
            name='client',
            field=models.ForeignKey(related_name='client', to='portal.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='officehour',
            name='admin',
            field=models.ForeignKey(to='portal.User'),
            preserve_default=True,
        ),
    ]
