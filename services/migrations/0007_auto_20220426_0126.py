# Generated by Django 3.2.7 on 2022-04-26 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='abbr',
            field=models.CharField(default='', max_length=20, unique=True, verbose_name='服务名缩写'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='abbr',
            field=models.CharField(max_length=20, unique=True, verbose_name='分类名缩写'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30, verbose_name='分类名'),
        ),
        migrations.AlterField(
            model_name='category',
            name='resume',
            field=models.TextField(default='', verbose_name='分类简介'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
    ]
