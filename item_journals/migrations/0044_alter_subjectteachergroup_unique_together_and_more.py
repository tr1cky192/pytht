# Generated by Django 4.2.14 on 2024-09-11 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item_journals', '0043_subjectteachergroup_groups'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subjectteachergroup',
            unique_together={('teacher', 'subject')},
        ),
        migrations.RemoveField(
            model_name='subjectteachergroup',
            name='group',
        ),
    ]
