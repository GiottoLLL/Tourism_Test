# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 18:09
# @Author  : GiottoLLL
# @Email   : GiottoLLL7@gmail.com
# @File    : adminx.py
# @Software: PyCharm
from .models import User
import xadmin


class UserAdmin(object):
    list_display = ('username', 'avatar_img', 'phone', 'email', 'background_img', 'sex')

xadmin.site.register(User, UserAdmin)
