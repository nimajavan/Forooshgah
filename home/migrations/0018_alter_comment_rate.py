# Generated by Django 3.2.8 on 2021-11-23 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
