# Generated by Django 4.2.14 on 2024-08-22 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item_journals', '0034_remove_subject_subgroups_remove_subject_teachers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='groups',
        ),
    ]
