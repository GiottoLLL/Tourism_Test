# -*- coding: utf-8 -*-
# @Time    : 2019/4/21 17:41
# @Author  : GiottoLLL
# @Email   : GiottoLLL7@gmail.com
# @File    : urls.py
# @Software: PyCharm
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static,serve
from . import views


urlpatterns = [
    path('', views.province, name='province'),
    path('', views.city, name='city'),
    path('', views.area, name='area')
]
