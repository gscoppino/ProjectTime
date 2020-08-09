# Generated by Django 2.2.1 on 2019-09-22 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_delete_task'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='charge',
            constraint=models.CheckConstraint(
                check=models.Q(
                    ('closed__exact', True),
                    ('end_time__exact', None),
                    _negated=True
                ),
                name='cannot_close_without_end_time'
            ),
        ),
    ]
