# Generated by Django 4.0.5 on 2024-07-30 12:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_mzalendo_updated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(120)], verbose_name=((0, 'Active'), (1, 'Completed'), (2, 'Due Date Passed'))),
        ),
    ]
