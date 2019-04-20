# Generated by Django 2.1.3 on 2019-04-17 16:42

import ckeditor_uploader.fields
from django.db import migrations
import stdimage.models
import stdimage.utils


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20190416_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=None, verbose_name='攻略'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to=stdimage.utils.UploadToUUID(path='avatar/20190418'), verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='background',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to=stdimage.utils.UploadToUUID(path='background/20190418'), verbose_name='背景图'),
        ),
    ]