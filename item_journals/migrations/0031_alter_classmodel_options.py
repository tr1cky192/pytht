# Generated by Django 4.2.14 on 2024-08-21 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item_journals', '0030_remove_classmodel_subgroup_alter_student_group_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classmodel',
            options={'verbose_name': 'заняття', 'verbose_name_plural': 'заняття'},
        ),
    ]
