# Generated by Django 4.2.14 on 2024-07-29 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item_journals', '0025_alter_subgroup_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsprogress',
            name='subgroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='item_journals.subgroup'),
        ),
    ]
