# Generated by Django 3.2.8 on 2021-11-16 07:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0015_alter_products_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='product_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='products',
            name='unlike',
            field=models.ManyToManyField(blank=True, related_name='product_unlike', to=settings.AUTH_USER_MODEL),
        ),
    ]
