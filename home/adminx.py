# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 18:09
# @Author  : GiottoLLL
# @Email   : GiottoLLL7@gmail.com
# @File    : adminx.py
# @Software: PyCharm
from .models import User, Strategy
import xadmin


class UserAdmin(object):
    list_display = ('username', 'avatar_img', 'phone', 'email', 'background_img', 'sex')

xadmin.site.register(User, UserAdmin)


class StrategyAdmin(object):
    list_display = ('title', 'up', 'collection', 'author')

xadmin.site.register(Strategy, StrategyAdmin)
