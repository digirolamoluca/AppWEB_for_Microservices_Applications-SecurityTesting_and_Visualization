# Generated by Django 3.2.9 on 2021-12-09 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20211209_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='macm',
            name='asset_types',
            field=models.CharField(max_length=100),
        ),
    ]
