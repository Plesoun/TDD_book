# Generated by Django 2.0 on 2019-10-30 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_list_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='text',
        ),
        migrations.AddField(
            model_name='item',
            name='list',
            field=models.TextField(default=''),
        ),
    ]
