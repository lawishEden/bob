# Generated by Django 3.2.9 on 2023-06-10 10:59

import book.Storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='书名')),
                ('rating', models.CharField(default='0', max_length=5, verbose_name='评分')),
                ('price', models.FloatField(default=0, verbose_name='价格')),
                ('cover', models.ImageField(default='img/default.png', storage=book.Storage.ImageStorage(), upload_to='upload/%Y/%m/%d', verbose_name='封面')),
                ('introduction', models.CharField(blank=True, default='', max_length=200, verbose_name='介绍')),
                ('publish', models.CharField(blank=True, default='', max_length=50, verbose_name='出版社')),
                ('url', models.URLField(blank=True, default='', verbose_name='URL')),
            ],
            options={
                'verbose_name': '图书管理',
                'verbose_name_plural': '图书管理',
            },
        ),
    ]
