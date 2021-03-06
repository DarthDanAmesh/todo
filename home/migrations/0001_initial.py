# Generated by Django 3.0.4 on 2020-05-25 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('date_assigned', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField()),
                ('status', models.IntegerField(default=0, verbose_name=((0, 'Active'), (1, 'Completed'), (2, 'Due Date Passed')))),
            ],
        ),
    ]
