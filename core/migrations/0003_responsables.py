# Generated by Django 5.0.6 on 2024-05-24 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_inventario_carrera_alter_inventario_digitador'),
    ]

    operations = [
        migrations.CreateModel(
            name='Responsables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
    ]
