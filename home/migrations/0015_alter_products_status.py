# Generated by Django 3.2.8 on 2021-11-15 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_products_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='status',
            field=models.CharField(blank=True, choices=[('None', 'none'), ('Size', 'size'), ('Color', 'color')], default=None, max_length=200, null=True),
        ),
    ]
