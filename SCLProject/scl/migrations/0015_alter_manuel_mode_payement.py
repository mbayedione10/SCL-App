# Generated by Django 3.2.6 on 2021-09-03 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scl', '0014_auto_20210903_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manuel',
            name='mode_payement',
            field=models.CharField(choices=[('Espéces', 'Espéces'), ('Chéque', 'Chéque')], default='Espéces', max_length=30),
        ),
    ]
