# Generated by Django 3.0.2 on 2021-01-25 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0016_auto_20210123_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='notas',
            name='HoraRegistro',
            field=models.DateTimeField(null=True),
        ),
    ]