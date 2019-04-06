from datetime import datetime
from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID


# Create your models here.
class User(models.Model):
    """普通用户表"""

    gender = (
        ('male', '男'),
        ('female', '女'),

    )
    username = models.CharField(max_length=128, verbose_name="用户名",  unique=True)
    password = models.CharField(max_length=256, verbose_name="密码")
    phone = models.CharField(
        max_length=13,
        verbose_name="手机号",
        blank=True
    )
    email = models.EmailField(blank=True, verbose_name="邮箱")
    sex = models.CharField(max_length=32, choices=gender, default='男', verbose_name="性别",blank=True)
    avatar = StdImageField(
        upload_to=UploadToUUID(path=datetime.now().strftime("avatar/%Y%m%d")),
        variations={'thumbnail': {'width': 100, 'height': 75}},
        null=True,
        blank=True,
        verbose_name="头像"
    )
    background = StdImageField(
        upload_to=UploadToUUID(path=datetime.now().strftime("background/%Y%m%d")),
        variations={'thumbnail': {'width': 100, 'height': 75}},
        null=True,
        blank=True,
        verbose_name="背景图"
    )
    sign = models.CharField(max_length=64, null=True, blank=True, verbose_name="一句话介绍")
    introduce = models.CharField(max_length=200, null=True, blank=True, verbose_name="个人简介")
    c_time = models.DateTimeField(auto_now_add=True)

    def avatar_img(self):
        if self.avatar:
            return str('<img src="%s" width="60" height="60" />' % self.avatar.url)
        else:
            return ' '

    avatar_img.short_description = '头像'
    avatar_img.allow_tags = True

    def background_img(self):
        if self.background:
            return str('<img src="%s" width="200" height="48" />' % self.background.url)
        else:
            return ' '

    background_img.short_description = '背景图'
    background_img.allow_tags = True

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['c_time']
        verbose_name = '旅途用户'
        verbose_name_plural = '旅途用户'

