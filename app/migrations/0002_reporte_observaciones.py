# Generated by Django 5.1.5 on 2025-02-12 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporte',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
    ]
