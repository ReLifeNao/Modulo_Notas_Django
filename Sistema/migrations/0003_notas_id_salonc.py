# Generated by Django 3.0.2 on 2021-01-15 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0002_auto_20210113_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='notas',
            name='Id_SalonC',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sistema.Salon'),
            preserve_default=False,
        ),
    ]