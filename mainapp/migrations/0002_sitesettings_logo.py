# Generated by Django 4.2.3 on 2024-07-13 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='logo',
            field=models.ImageField(default='', upload_to='site-settings'),
            preserve_default=False,
        ),
    ]
