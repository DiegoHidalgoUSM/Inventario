# Generated by Django 5.0.6 on 2024-05-23 15:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='carreras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Etiqueta', models.CharField(max_length=50)),
                ('Numero_Serie', models.CharField(max_length=50)),
                ('Descripcion_Equipamiento', models.CharField(max_length=50)),
                ('Responsable', models.CharField(max_length=50)),
                ('Ubicacion', models.CharField(max_length=50)),
                ('Observacion', models.CharField(max_length=50)),
                ('Carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.carreras')),
                ('Digitador', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
