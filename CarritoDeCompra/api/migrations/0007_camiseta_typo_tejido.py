# Generated by Django 4.2.7 on 2023-11-30 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_tejido_alter_camiseta_stock_initial_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='camiseta',
            name='typo_tejido',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.tejido'),
        ),
    ]
