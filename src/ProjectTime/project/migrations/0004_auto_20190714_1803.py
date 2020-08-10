# Generated by Django 2.2.1 on 2019-07-14 18:03

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20190714_1720'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='charge',
            name='end_time_greater_than_start_time',
        ),
        migrations.AddConstraint(
            model_name='charge',
            constraint=models.CheckConstraint(
                check=models.Q(
                    end_time__gte=django.db.models.expressions.F('start_time')
                ),
                name='end_time_must_be_on_or_after_start_time'
            ),
        ),
    ]
