# Generated by Django 3.2.8 on 2021-11-24 11:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0018_alter_comment_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_like',
            field=models.ManyToManyField(blank=True, related_name='com_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
