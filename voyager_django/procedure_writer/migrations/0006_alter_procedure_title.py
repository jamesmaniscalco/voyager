# Generated by Django 4.2.3 on 2023-07-27 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedure_writer', '0005_alter_datafield_procedure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='procedure',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
