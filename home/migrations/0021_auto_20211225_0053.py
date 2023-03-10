# Generated by Django 3.2.8 on 2021-12-24 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='color',
            field=models.ManyToManyField(blank=True, to='home.Color'),
        ),
        migrations.AddField(
            model_name='products',
            name='size',
            field=models.ManyToManyField(blank=True, to='home.Size'),
        ),
        migrations.AddField(
            model_name='products',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.brand'),
        ),
    ]
