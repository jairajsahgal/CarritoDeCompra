# Generated by Django 4.2.7 on 2023-11-30 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_mangas_camiseta_con_mangas'),
    ]

    operations = [
        migrations.AddField(
            model_name='camiseta',
            name='imagen',
            field=models.URLField(blank=True, default='https://placehold.co/600x400/png', null=True),
        ),
        migrations.AddField(
            model_name='gorras',
            name='imagen',
            field=models.URLField(blank=True, default='https://placehold.co/600x400/png', null=True),
        ),
    ]
