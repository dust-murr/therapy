# Generated by Django 3.2.12 on 2022-04-12 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('therapy', '0007_auto_20220409_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='email',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='therapist_id',
        ),
        migrations.RemoveField(
            model_name='therapist',
            name='email',
        ),
    ]
