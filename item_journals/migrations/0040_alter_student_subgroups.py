# Generated by Django 4.2.14 on 2024-09-11 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_journals', '0039_alter_student_subgroups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='subgroups',
            field=models.ManyToManyField(blank=True, related_name='subgroups', to='item_journals.subgroup', verbose_name='Підгрупи'),
        ),
    ]
