# Generated by Django 5.0.6 on 2024-05-23 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='Carrera',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='Digitador',
            field=models.CharField(max_length=50),
        ),
    ]
