# Generated by Django 3.2.12 on 2022-05-08 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('therapy', '0014_auto_20220507_2136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discharge',
            name='email',
        ),
    ]
