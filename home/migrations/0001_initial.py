# Generated by Django 2.1.3 on 2019-04-04 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=13, unique=True, verbose_name='手机号')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=32)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar/%Y%m%d')),
                ('background', models.ImageField(blank=True, null=True, upload_to='background/%Y%m%d')),
                ('sign', models.CharField(max_length=64, null=True)),
                ('introduce', models.CharField(max_length=200, null=True)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
