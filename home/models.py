from datetime import datetime
from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID
from ckeditor_uploader.fields import RichTextUploadingField


class Tags(models.Model):
    tag_name = models.CharField(max_length=50, verbose_name='标签名')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.tag_name


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
    sex = models.CharField(max_length=32, choices=gender, default='男', verbose_name="性别", blank=True)
    avatar = StdImageField(
        upload_to=UploadToUUID(path=datetime.now().strftime("avatar/%Y%m%d")),
        variations={'thumbnail': {'width': 100, 'height': 75, 'style': 'objects-fit:cover'}},
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
    sign = models.CharField(max_length=64, null=True, blank=True, verbose_name="一句话介绍", default='该用户还没有个性签名')
    introduce = models.CharField(max_length=200, null=True, blank=True, verbose_name="个人简介", default='该用户还没有个人简介')
    c_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tags, related_name='user_pick', blank=True)

    def avatar_img(self):
        if self.avatar:
            return str('<img src="%s" width="60" height="60" style="object-fit: cover" />' % self.avatar.url)
        else:
            return ' '

    avatar_img.short_description = '头像'
    avatar_img.allow_tags = True

    def background_img(self):
        if self.background:
            return str('<img src="%s" width="200" height="48"  style="object-fit:cover"/>' % self.background.url)
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


class Strategy(models.Model):
    state = (
        ('review', '审核中'),
        ('publish', '已发布'),
        ('nopass', '建议修改')
    )
    title = models.CharField(max_length=100, blank=True)
    content = RichTextUploadingField(verbose_name='攻略', default=None, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    img = StdImageField(
        upload_to=UploadToUUID(path=datetime.now().strftime("strategy/%Y%m%d")),
        variations={'thumbnail': {'width': 160, 'height': 100}},
        null=True,
        blank=True,
        verbose_name="题图"
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    s_state = models.CharField(max_length=32, choices=state, default='审核中', verbose_name="攻略状态", blank=True)
    users_like_count = models.IntegerField(blank=True, verbose_name="点赞数", default=0)
    users_like = models.ManyToManyField(User, related_name="strategy_like", blank=True)
    collections_count = models.IntegerField(blank=True, verbose_name="收藏数", default=0)
    collections = models.ManyToManyField(User, related_name="strategy_collections", blank=True)
    comment_count = models.IntegerField(blank=True, verbose_name="点赞数", default=0)
    tags = models.ManyToManyField(Tags, related_name='strategy_pick', blank=True)

    def strategy_img(self):
        if self.img:
            return str('<img src="%s" width="60" height="60" style="object-fit: cover" />' % self.img.url)
        else:
            return ' '

    strategy_img.short_description = '头像'
    strategy_img.allow_tags = True

    class Meta:
        ordering = ("title", )
        verbose_name = '攻略文章'
        verbose_name_plural = '攻略文章'

    def __str__(self):
        return self.title


class Comment(models.Model):#同一个model引用两个外键必须要指定不同的related_name
    """
    评论功能
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者', related_name="comment_author")
    content = models.CharField(max_length=300, verbose_name='评论内容')
    to_someone = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='回复某人', null=True, related_name="comment_to")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, verbose_name='攻略')

    class Meta:
        verbose_name = '评论攻略'
        verbose_name_plural = '评论攻略'

    def __str__(self):
        return self.content[:10]


class New(models.Model):#同一个model引用两个外键必须要指定不同的related_name
    """
    新私信提醒
    """
    status = {
        ('nomal', '正常'),
        ('black', '屏蔽'),
    }
    new_send_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发送者', related_name="new_send_user")
    content = models.CharField(max_length=300, verbose_name='私信内容')
    new_to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='回复某人',
                                null=True, related_name="new_to_user")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pull_black = models.CharField(max_length=32, choices=status, default='正常', verbose_name="状态", blank=True)

    class Meta:
        verbose_name = '新私信'
        verbose_name_plural = '新私信'

    def __str__(self):
        return self.content[:10]


class Chat(models.Model):#同一个model引用两个外键必须要指定不同的related_name
    """
    私信
    """
    status = {
        ('nomal', '正常'),
        ('black', '屏蔽'),
    }
    send_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发送者', related_name="send_user")
    content = models.CharField(max_length=300, verbose_name='私信内容')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='回复某人', null=True, related_name="to_user")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pull_black = models.CharField(max_length=32, choices=status, default='正常', verbose_name="状态", blank=True)

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = '私信'

    def __str__(self):
        return self.content[:10]


class Follow(models.Model):
    follow = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    fan = models.ForeignKey(User, related_name='fan_user', on_delete=models.CASCADE)

    def __str__(self):
        return "follow:{},fan:{}".format(self.follow, self.fan)


class Report(models.Model):
    """
    举报表
    """
    item = (
        ('spam', '垃圾信息'),
        ('unfriendly', '不友善信息'),
        ('harm', '有害信息'),
        ('tort', '涉嫌侵权'),
        ('other', '其他'),
    )
    target = models.ForeignKey(User, verbose_name='目标', related_name='target', on_delete=models.CASCADE)
    report = models.ForeignKey(User, verbose_name='举报者', blank=True, null=True, related_name='report', on_delete=models.CASCADE)
    reason = models.CharField(max_length=32, choices=item, default='男', verbose_name="性别", blank=True)
    details = models.CharField(max_length=500, blank=True, null=True)
    lock_time = models.DateTimeField(verbose_name='开始封禁时间', blank=True, null=True)
    unlock_time = models.DateTimeField(verbose_name='解除封禁时间', blank=True, null=True)

    class Meta:
        verbose_name = '封禁'
        verbose_name_plural = '封禁'

    def __str__(self):
        return self.reason
