# Generated by Django 3.2.13 on 2022-05-10 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20220510_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='store.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=200),
        ),
    ]
