# Generated by Django 4.2.3 on 2024-07-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicepage',
            name='image',
        ),
        migrations.AddField(
            model_name='servicepage',
            name='sub_titless',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
