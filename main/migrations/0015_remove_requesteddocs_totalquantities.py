# Generated by Django 4.0 on 2021-12-14 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_rename_i_requesteddocs_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requesteddocs',
            name='TotalQuantities',
        ),
    ]
