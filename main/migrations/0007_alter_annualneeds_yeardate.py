# Generated by Django 4.0 on 2021-12-14 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_annualneeds_yeardate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annualneeds',
            name='YearDate',
            field=models.DateField(),
        ),
    ]
