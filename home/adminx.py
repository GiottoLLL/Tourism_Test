# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 18:09
# @Author  : GiottoLLL
# @Email   : GiottoLLL7@gmail.com
# @File    : adminx.py
# @Software: PyCharm
from .models import User, Strategy, Comment, Tags, Report
import xadmin


class UserAdmin(object):
    list_display = ('username', 'avatar_img', 'phone', 'email', 'background_img', 'sex', 'tags')

xadmin.site.register(User, UserAdmin)


class StrategyAdmin(object):
    list_display = ('title', 'author', 'tags', 's_state')

xadmin.site.register(Strategy, StrategyAdmin)


class CommentAdmin(object):
    list_display = ('content', 'strategy', 'author', 'to_someone')

xadmin.site.register(Comment, CommentAdmin)


class TagsAdmin(object):
    list_display = ('tag_name',)

xadmin.site.register(Tags, TagsAdmin)


class ReportAdmin(object):
    list_display = ('target', 'report', 'reason', 'details', 'lock_time', 'unlock_time')

xadmin.site.register(Report, ReportAdmin)
