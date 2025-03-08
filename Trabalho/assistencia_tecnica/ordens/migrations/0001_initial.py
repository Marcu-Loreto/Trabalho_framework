# Generated by Django 4.2.20 on 2025-03-08 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_serie', models.CharField(max_length=50, unique=True)),
                ('modelo', models.CharField(max_length=100)),
                ('ano_fabricacao', models.PositiveIntegerField()),
                ('tempo_garantia', models.CharField(max_length=50)),
                ('data_vigencia_garantia', models.DateField()),
            ],
        ),
    ]
