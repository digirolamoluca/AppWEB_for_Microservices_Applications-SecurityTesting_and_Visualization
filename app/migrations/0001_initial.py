# Generated by Django 3.2.9 on 2021-12-09 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MACM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appId', models.IntegerField(null=True)),
                ('application', models.CharField(max_length=100)),
                ('components', models.CharField(max_length=100)),
                ('primaries', models.CharField(max_length=100)),
                ('secondaries', models.CharField(max_length=100)),
                ('asset_type', models.CharField(max_length=100)),
                ('dev_types', models.CharField(max_length=100)),
                ('custom_types', models.CharField(max_length=100)),
            ],
        ),
    ]
