# Generated by Django 3.1.7 on 2021-03-03 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlsmodel',
            name='uid',
            field=models.CharField(default='0000000', max_length=300, verbose_name='Video Unique ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videosmodel',
            name='title',
            field=models.CharField(max_length=300, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='videosmodel',
            name='uid',
            field=models.CharField(default='000000', max_length=300, unique=True, verbose_name='UID'),
        ),
        migrations.AlterField(
            model_name='videosmodel',
            name='uploader',
            field=models.CharField(max_length=300, verbose_name='Uploader'),
        ),
        migrations.AlterField(
            model_name='videosmodel',
            name='url',
            field=models.URLField(verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='videosmodel',
            name='views_count',
            field=models.IntegerField(verbose_name='Views'),
        ),
    ]