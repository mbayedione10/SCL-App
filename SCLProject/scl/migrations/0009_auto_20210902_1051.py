# Generated by Django 3.2.6 on 2021-09-02 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scl', '0008_auto_20210902_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affaire',
            name='montant',
            field=models.IntegerField(default=0, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='manuel',
            name='montant',
            field=models.IntegerField(default=0, max_length=50, null=True),
        ),
    ]
