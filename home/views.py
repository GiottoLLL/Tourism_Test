from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from home import models
from .form import UserForm, RegisterForm, WriteForm
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
            strategy = models.Strategy.objects.all().order_by('id')
            return render(request, 'home/index.html',locals())
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


def detail_page(request, strategy_id):
    """
    攻略详情页面
    :param request: 
    :return: 
    """

    strategy = models.Strategy.objects.get(id=strategy_id)
    return render(request, 'home/detail_page.html', locals())


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


def write_page(request):
    """
    写攻略页面
    :param request: 
    :return: 
    """
    if request.session.get('is_login', None):
        if request.session['is_login'] is not True:
            return redirect('login')
    if request.method == "POST":
        write_form = WriteForm(request.POST)
        if write_form.is_valid():
            title = write_form.cleaned_data['title']
            content = write_form.cleaned_data['content']
            user_id = request.session['user_id']
            user = models.User.objects.get(id=user_id)

            # 创建新文章
            new_strategy = models.Strategy.objects.create(
                title=title,
                content=content,
                author_id=user_id,
                s_state='review'
            )
            new_strategy.save()
            return render(request, 'home/write_page.html', {'success': '发布成功'})
        else:
            message = "上传出错，请重试"
            return render(request, 'home/write_page.html', locals())
    write_form = WriteForm()
    return render(request, 'home/write_page.html', locals())


def up_add(request, strategy_id):
    """点赞设置"""
    if request.is_ajax():
        strategy = models.Strategy.objects.filter(id=strategy_id)[0]
        strategy.up += 1
        strategy.save()
        result = {'type': 'ok'}
        return JsonResponse(result)

@csrf_exempt
def like_strategy(request):
    strategy_id = request.POST.get("id")
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    if strategy_id:
        try:
            strategy = models.Strategy.objects.get(id=strategy_id)
            if models.Strategy.objects.filter(users_like=user_id):
                strategy.users_like.remove(user)
                sum = strategy.users_like.count()
                result = {'type': 'down',
                          'sum': sum}
                return JsonResponse(result)
            else:
                strategy.users_like.add(user)
                sum = strategy.users_like.count()
                result = {'type': 'up',
                          'sum': sum}
                return JsonResponse(result)
        except:
            result = {'type': 'error'}
            return JsonResponse(result)
