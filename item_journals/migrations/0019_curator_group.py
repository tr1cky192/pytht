# Generated by Django 4.2.14 on 2024-07-27 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item_journals', '0018_merge_20240727_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='curator',
            name='group',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curator_relation', to='item_journals.collagegroups', verbose_name='Група'),
        ),
    ]
