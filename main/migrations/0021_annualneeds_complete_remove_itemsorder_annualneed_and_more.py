# Generated by Django 4.0 on 2021-12-19 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_users_delete_requesteddocs_annualneeds_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='annualneeds',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='itemsorder',
            name='annualneed',
        ),
        migrations.AddField(
            model_name='itemsorder',
            name='annualneed',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.annualneeds'),
            preserve_default=False,
        ),
    ]
