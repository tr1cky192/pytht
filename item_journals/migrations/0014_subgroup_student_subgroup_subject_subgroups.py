# Generated by Django 5.0.3 on 2024-07-26 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_journals', '0013_collagegroups_curator_alter_curator_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subgroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('parent_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subgroups', to='item_journals.collagegroups')),
            ],
            options={
                'verbose_name': 'підгрупа',
                'verbose_name_plural': 'підгрупи',
                'db_table': 'subgroups',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='subgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='item_journals.subgroup'),
        ),
        migrations.AddField(
            model_name='subject',
            name='subgroups',
            field=models.ManyToManyField(blank=True, related_name='subjects', to='item_journals.subgroup', verbose_name='підгрупи'),
        ),
    ]
