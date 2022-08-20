# Generated by Django 3.2 on 2022-08-11 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0007_auto_20220811_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holdings',
            name='bid_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ohlcv',
            name='close_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ohlcv',
            name='high_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ohlcv',
            name='low_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ohlcv',
            name='open_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='orders',
            name='bid_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='users',
            name='available_funds',
            field=models.DecimalField(decimal_places=2, default=400000, max_digits=10),
        ),
        migrations.AlterField(
            model_name='users',
            name='blocked_funds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]