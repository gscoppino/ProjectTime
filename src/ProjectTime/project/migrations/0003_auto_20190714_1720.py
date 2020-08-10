# Generated by Django 2.2.1 on 2019-07-14 17:20

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20190714_1617'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='charge',
            name='start_time_less_than_end_time',
        ),
        migrations.AddConstraint(
            model_name='charge',
            constraint=models.CheckConstraint(
                check=models.Q(
                    end_time__gte=django.db.models.expressions.F('start_time')
                ),
                name='end_time_greater_than_start_time'
            ),
        ),
    ]
