# Generated by Django 3.2.8 on 2021-12-17 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20211024_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='1.png', upload_to='profile/'),
        ),
    ]
