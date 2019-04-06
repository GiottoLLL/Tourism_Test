from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from home import models
from .form import UserForm, RegisterForm
import hashlib


# Create your views here.

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    """
    主页
    :param request: 
    :return: 
    """
    if request.session.get('is_login', None):
        if request.session['is_login'] is not True:
            return redirect('login')
        else:
            return render(request, 'home/index.html', {
            'titles': ['推荐', '关注', '热门'],
            'my_content': ['我的主页', '我的攻略', '设置'],
            })
    else:
        return redirect('login')


def login_page(request):
    """
    用户登录界面 
    :param request: 
    :return: 
    """
    if request.session.get('is_login', None) is True:
        return redirect('index')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(username=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return redirect('index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'home/login_page.html', locals())
    login_form = UserForm()
    return render(request, 'home/login_page.html', locals())


def logout_page(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("index")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("login")


def register_page(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            phone = register_form.cleaned_data['phone']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'home/login_page.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'home/login_page.html', locals())
                same_email_user = models.User.objects.filter(phone=phone)
                if same_email_user:  # 手机号码地址唯一
                    message = '该手机号已被注册，请使用别的号码！'
                    return render(request, 'home/login_page.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = models.User.objects.create()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.phone = phone
                new_user.sex = sex
                new_user.save()
                return redirect('login')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'home/register_page.html', locals())


def person_page(request):
    """
    个人中心
    :param request: 
    :return: 
    """
    return render(request, 'home/person_page.html', {
        'titles': ['推荐', '关注', '热门'],
        'my_content': ['我的主页', '我的攻略', '设置']
    })


def detail_page(request):
    """
    攻略详情页面
    :param request: 
    :return: 
    """
    return render(request, 'home/detail_page.html', {
        'titles': ['推荐', '关注', '热门'],
        'my_content': ['我的主页', '我的攻略', '设置']
    })


def edit_page(request):
    """
    个人资料编辑
    :param request: 
    :return: 
    """
    return render(request, 'home/edit_page.html', {
        'titles': ['推荐', '关注', '热门'],
        'my_content': ['我的主页', '我的攻略', '设置']
    })
