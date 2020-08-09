# Generated by Django 2.2.1 on 2019-09-21 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20190921_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='active',
            field=models.BooleanField(
                blank=True,
                default=True,
                help_text='An inactive project is disabled for modification.'
            ),
        ),
    ]
