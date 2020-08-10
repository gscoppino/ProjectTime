# Generated by Django 2.2.1 on 2019-09-08 01:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20190714_1803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False,
                                        verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('deadline', models.DateTimeField()),
                ('done', models.BooleanField(blank=True, default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                              to='project.Project')),
            ],
            options={
                'ordering': ('deadline', 'done'),
            },
        ),
    ]
