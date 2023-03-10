# Generated by Django 4.0 on 2021-12-14 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_annualneeds_yeardate'),
    ]

    operations = [
        migrations.AddField(
            model_name='annualneeds',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Being Reviewed', 'Being Reviewed'), ('Needs Alteration', 'Needs Alteration'), ('Approved', 'Out Door')], default='Pending', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='annualneeds',
            name='Faculity',
            field=models.CharField(choices=[('IT', 'IT'), ('ARCHITECTURE', 'ARCHITECTURE'), ('MEDICINE', 'MEDICINE'), ('PHARMACY', 'PHARMACY'), ('DENTISTRY', 'DENTISTRY'), ('BUSINESS', 'BUSINESS')], max_length=200, null=True),
        ),
    ]
