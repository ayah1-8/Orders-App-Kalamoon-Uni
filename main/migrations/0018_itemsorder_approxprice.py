# Generated by Django 4.0 on 2021-12-16 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_remove_itemsall_tag_itemsall_tagname_delete_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemsorder',
            name='ApproxPrice',
            field=models.FloatField(default=0),
        ),
    ]
