from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from home import models
from .form import UserForm, RegisterForm, WriteForm, CommentForm, ReportForm
import hashlib, os
from django.core import serializers
from django.utils import timezone


# Create your views here.
def hash_code(s, salt='mysite'):  # 加点盐
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
            user_id = request.session['user_id']
            user = models.User.objects.get(id=user_id)
            strategy = models.Strategy.objects.filter(s_state='publish').order_by('-users_like_count', )
            collection_count = 0
            user_collection = models.Strategy.objects.filter(collections=user_id)
            fans = models.Follow.objects.filter(follow_id=user_id)
            follow = models.Follow.objects.filter(fan_id=user_id)
            if models.New.objects.filter(new_to_user=user_id):
                new = models.New.objects.filter(new_to_user=user_id).count()
            return render(request, 'home/index.html', locals())
    else:
        return redirect('login')


def hot(request):
    """
    热门
    :param request: 
    :return: 
    """
    if request.session.get('is_login', None):
        if request.session['is_login'] is not True:
            return redirect('login')
        else:
            user_id = request.session['user_id']
            user = models.User.objects.get(id=user_id)
            strategy = models.Strategy.objects.objects.filter(s_state='publish').order_by('-users_like_count', )
            collection_count = 0
            user_collection = models.Strategy.objects.filter(collections=user_id)
            fans = models.Follow.objects.filter(follow_id=user_id)
            follow = models.Follow.objects.filter(fan_id=user_id)
            if models.New.objects.filter(new_to_user=user_id):
                new = models.New.objects.filter(new_to_user=user_id).count()
            return render(request, 'home/index.html', locals())
    else:
        return redirect('login')


def recommend(request):
    """
    推荐
    :param request: 
    :return: 
    """
    if request.session.get('is_login', None):
        if request.session['is_login'] is not True:
            return redirect('login')
        else:
            user_id = request.session['user_id']
            user = models.User.objects.get(id=user_id)
            tags = models.Tags.objects.filter(user_pick=request.session['user_id'])
            strategy = []
            user_collection = models.Strategy.objects.filter(collections=user_id)
            collection_count = 0
            fans = models.Follow.objects.filter(follow_id=user_id)
            follow = models.Follow.objects.filter(fan_id=user_id)
            for tag in tags:
                s = models.Strategy.objects.filter(tags=tag.id, s_state='publish')
                strategy += s
            if models.New.objects.filter(new_to_user=user_id):
                new = models.New.objects.filter(new_to_user=user_id).count()
            return render(request, 'home/index.html', locals())
    else:
        return redirect('login')


def search(request):
    q = request.GET.get('q')
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    if not q:
        error_msg = '请输入关键字'
        return render(request, 'home/index.html', {'error_msg': error_msg})
    strategy = models.Strategy.objects.filter(Q(title__icontains=q, s_state='publish') | Q(content__icontains=q, s_state='publish'))
    collection_count = 0
    user_collection = models.Strategy.objects.filter(collections=user_id)
    fans = models.Follow.objects.filter(follow_id=user_id)
    follow = models.Follow.objects.filter(fan_id=user_id)
    if models.New.objects.filter(new_to_user=user_id):
        new = models.New.objects.filter(new_to_user=user_id).count()
    return render(request, 'home/index.html', locals())


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
                if models.Report.objects.filter(target=user, report=None):
                    lock = models.Report.objects.get(target=user, report=None).lock_time
                    unlock = models.Report.objects.get(target=user, report=None).unlock_time
                    data_now = timezone.now()
                    if lock < data_now < unlock:
                        message = "您已被禁止登录"
                        return render(request, 'home/login_page.html', locals())
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


@csrf_exempt
def register_page(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if request.POST:  # 获取数据
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            phone = request.POST.get('phone')
            sex = request.POST.get('sex')
            tags = request.POST.getlist('tags')
            if not username or not password1 or not password2 or not phone or not sex:
                result = {'status': '注册信息不完整！'}
                return JsonResponse(result)
            if password1 != password2:  # 判断两次密码是否相同
                result = {'status': '两次输入的密码不同！'}
                return JsonResponse(result)
            else:
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    result = {'status': '用户已经存在，请重新选择用户名！'}
                    return JsonResponse(result)
                same_email_user = models.User.objects.filter(phone=phone)
                if same_email_user:  # 手机号码地址唯一
                    result = {'status': '该手机号已被注册，请使用别的号码！'}
                    return JsonResponse(result)

                # 当一切都OK的情况下，创建新用户
                new_user = models.User.objects.create(
                    username=username,
                    password=hash_code(password1),
                    phone=phone,
                    sex=sex,
                )
                new_user.save()
                if tags:
                    user = models.User.objects.get(username=username)
                    for foo in tags:
                        tag1 = models.Tags.objects.get(id=foo)
                        user.tags.add(tag1)
                result = {'status': '注册成功'}
                return JsonResponse(result)
    register_form = RegisterForm()
    tag = models.Tags.objects.all()
    return render(request, 'home/register_page.html', locals())


def person_page(request, tab):
    """
    个人中心（自己的）
    :param request: 
    :return: 
    """
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    collection = user.strategy_collections.all()
    strategy = models.Strategy.objects.filter(author=user_id)
    user_comment = models.Comment.objects.filter(author=user_id)
    user_like = models.Strategy.objects.filter(users_like=user_id)
    user_collection = models.Strategy.objects.filter(collections=user_id)
    up_count = 0
    collection_count = 0
    fans = models.Follow.objects.filter(follow_id=user_id)
    follow = models.Follow.objects.filter(fan_id=user_id)
    tab = tab
    self = 1
    for item in strategy:
        up_count += item.users_like_count
        collection_count += item.collections_count
    status = -1
    return render(request, 'home/person_page.html', locals())


def anotherone_page(request, id, tab):
    """
    个人中心（别人的）
    :param request: 
    :return: 
    """
    another_id = id
    if another_id == request.session['user_id']:
        user_id = request.session['user_id']
        user = models.User.objects.get(id=user_id)
        collection = user.strategy_collections.all()
        strategy = models.Strategy.objects.filter(author=user_id)
        user_collection = models.Strategy.objects.filter(collections=user_id)
        up_count = 0
        collection_count = 0
        fans = models.Follow.objects.filter(follow_id=user_id)
        follow = models.Follow.objects.filter(fan_id=user_id)
        self = 1
        for item in strategy:
            up_count += item.users_like_count
            collection_count += item.collections_count
        status = -1
        return render(request, 'home/person_page.html', locals())
    else:
        self_id = request.session['user_id']
        self_avatar = models.User.objects.get(id=self_id).avatar
        user = models.User.objects.get(id=another_id)
        collection = user.strategy_collections.all()
        strategy = models.Strategy.objects.filter(author=another_id)
        user_collection = models.Strategy.objects.filter(collections=another_id)
        up_count = 0
        collection_count = 0
        fans = models.Follow.objects.filter(follow_id=another_id)
        follow = models.Follow.objects.filter(fan_id=another_id)
        self = 0
        for item in strategy:
            up_count += item.users_like_count
            collection_count += item.collections_count
        status = 1
        return render(request, 'home/person_page.html', locals())


def detail_page(request, strategy_id):
    """
    攻略详情页面
    :param request: 
    :return: 
    """
    comment_form = CommentForm()
    report_form = ReportForm()
    strategy = models.Strategy.objects.get(id=strategy_id)
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    tags = strategy.tags.all()
    if strategy.author_id == user_id:
        author = 0
    else:
        author = 1
        if models.Follow.objects.filter(follow_id=strategy.author_id, fan_id=user_id):
            follow_status = 1
        else:
            follow_status = 0
    if models.Strategy.objects.filter(collections=user, id=strategy_id):
        col = 1
    else:
        col = 0
    if models.Strategy.objects.filter(users_like=user, id=strategy_id):
        like = 1
    else:
        like = 0
    if models.Comment.objects.filter(strategy_id=strategy_id):
        comment = models.Comment.objects.filter(strategy_id=strategy_id).order_by('-create_time')
    fans = models.Follow.objects.filter(follow_id=strategy.author_id)
    follow = models.Follow.objects.filter(fan_id=strategy.author_id)
    collections = models.User.objects.filter(strategy_collections=strategy_id)
    return render(request, 'home/detail_page.html', locals())


def edit_page(request):
    """
    个人资料编辑页面
    :param request: 
    :return: 
    """
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    tags = user.tags.all()
    tags_all = models.Tags.objects.all()
    return render(request, 'home/edit_page.html', locals())


@csrf_exempt
def change(request):
    """
    编辑个人资料
    :param request: 
    :return: 
    """
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    if request.POST.get("username"):
        new_username = request.POST.get("username")
        user.username = new_username
        user.save()
        result = {'status': '修改成功',
                  'changed': new_username}
    if request.POST.get("sex"):
        new_sex = request.POST.get("sex")
        user.sex = new_sex
        user.save()
        result = {'status': '修改成功',
                  'changed': new_sex}
    if request.POST.get("sign"):
        new_sign = request.POST.get("sign")
        user.sign = new_sign
        user.save()
        result = {'status': '修改成功',
                  'changed': new_sign}
    if request.POST.get("tag"):
        tag = request.POST.get("tag")
        tags = models.Tags.objects.get(id=tag)
        user.tags.add(tags)
    if request.POST.get("introduce"):
        new_introduce = request.POST.get("introduce")
        user.introduce = new_introduce
        user.save()
        result = {'status': '修改成功',
                  'changed': new_introduce}
    if request.FILES.get("avatar"):
        new_avatar = request.FILES.get("avatar")
        user.avatar = new_avatar
        user.save()
        result = {'status': '修改成功'}
    if request.FILES.get("background"):
        new_background = request.FILES.get("background")
        user.background = new_background
        user.save()
        result = {'status': '修改成功'}
    if request.POST.get('tag_del'):
        tag = request.POST.get("tag_del")
        tags = models.Tags.objects.get(id=tag)
        user.tags.remove(tags)
        result = {'status': '删除成功',
                  'changed': request.POST.get("username")}
    return JsonResponse(result)


def write_page(request):
    """
    写攻略页面
    :param request: 
    :return: 
    """
    import time
    if request.session.get('is_login', None):
        if request.session['is_login'] is not True:
            return redirect('login')
    if request.method == "POST":
        write_form = WriteForm(request.POST, request.FILES)
        if write_form.is_valid():
            title = write_form.cleaned_data['title']
            content = write_form.cleaned_data['content']
            img = request.FILES.get('img')
            time = time.strftime('%Y%m%d%H%M%S')
            ext = os.path.splitext(img.name)[1]
            img.name = time + ext
            user_id = request.session['user_id']
            user = models.User.objects.get(id=user_id)

            # 创建新文章
            new_strategy = models.Strategy.objects.create(
                title=title,
                content=content,
                author_id=user_id,
                s_state='review',
                img=img
            )
            new_strategy.save()
            message = "发布成功"
            return render(request, 'home/write_page.html', locals())
        else:
            message = "上传出错，请重试"
            return render(request, 'home/write_page.html', locals())
    write_form = WriteForm()
    return render(request, 'home/write_page.html', locals())


@csrf_exempt
def like_strategy(request):
    """
    点赞
    :param request: 
    :return: 
    """
    strategy_id = request.POST.get("id")
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    if strategy_id:
        try:
            strategy = models.Strategy.objects.get(id=strategy_id)
            if models.Strategy.objects.filter(users_like=user_id, id=strategy_id):
                strategy.users_like.remove(user)
                sum = strategy.users_like.count()
                models.Strategy.objects.filter(id=strategy_id).update(
                    users_like_count=sum
                )
                result = {'type': 'down',
                          'sum': sum}
                return JsonResponse(result)
            else:
                strategy.users_like.add(user)
                sum = strategy.users_like.count()
                models.Strategy.objects.filter(id=strategy_id).update(
                    users_like_count=sum
                )
                result = {'type': 'up',
                          'sum': sum}
                return JsonResponse(result)
        except:
            result = {'type': 'error'}
            return JsonResponse(result)


@csrf_exempt
def collection_strategy(request):
    """
    收藏
    :param request: 
    :return: 
    """
    strategy_id = request.POST.get("id")
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    if strategy_id:
        try:
            strategy = models.Strategy.objects.get(id=strategy_id)
            if models.Strategy.objects.filter(collections=user_id, id=strategy_id):
                strategy.collections.remove(user)
                sum = strategy.collections.count()
                models.Strategy.objects.filter(id=strategy_id).update(
                    collections_count=sum
                )
                result = {'type': 'uncoll',
                          'sum': sum}
                return JsonResponse(result)
            else:
                strategy.collections.add(user)
                sum = strategy.collections.count()
                models.Strategy.objects.filter(id=strategy_id).update(
                    collections_count=sum
                )
                result = {'type': 'coll',
                          'sum': sum}
                return JsonResponse(result)
        except:
            result = {'type': 'error'}
            return JsonResponse(result)


@csrf_exempt
def comment(request):
    """
    评论
    """
    if request.POST.get("to_someone"):  # 有此字段则为回复
        user_id = request.session['user_id']
        # author = models.User.objects.get(id=user_id)
        content = request.POST.get("content")
        strategy_id = request.POST.get("strategy")
        # strategy = models.Strategy.objects.get(id=strategy_id)
        to_someone_id = request.POST.get("to_someone")
        # to_some = models.User.objects.get(id=to_some_id)

        # 创建新回复
        new_comment = models.Comment.objects.create(
            author_id=user_id,
            content=content,
            strategy_id=strategy_id,
            to_someone_id=to_someone_id
        )
        count = models.Comment.objects.filter(strategy_id=strategy_id).count()
        models.Strategy.objects.filter(id=strategy_id).update(
            comment_count=count
        )
        new_comment.save()
        result = {'status': '回复成功'}
        return JsonResponse(result)
    else:
        user_id = request.session['user_id']
        # author = models.User.objects.get(id=user_id)
        content = request.POST.get("content")
        strategy_id = request.POST.get("strategy")
        # strategy = models.Strategy.objects.get(id=strategy_id)

        # 创建新回复
        new_comment = models.Comment.objects.create(
            author_id=user_id,
            content=content,
            strategy_id=strategy_id
        )
        count = models.Comment.objects.filter(strategy_id=strategy_id).count()
        models.Strategy.objects.filter(id=strategy_id).update(
            comment_count=count
        )
        new_comment.save()
        result = {'status': '评论成功'}
        return JsonResponse(result)


@csrf_exempt
def send_chat(request):
    if request.POST:
        send_user_id = request.session['user_id']
        send_user = models.User.objects.get(id=send_user_id)
        content = request.POST.get("content")
        to_user_id = request.POST.get("to_user")
        to_user = models.User.objects.get(id=to_user_id)
        pull_black = 'nomal'
        new_news = models.New.objects.create(
            new_send_user=send_user,
            content=content,
            new_to_user=to_user,
            pull_black=pull_black,
        )
        new_news.save()
        new_chat = models.Chat.objects.create(
            send_user=send_user,
            content=content,
            to_user=to_user,
            pull_black=pull_black,
        )
        new_chat.save()
        result = {'status': '发送成功'}
        return JsonResponse(result)


def open_chat(request):
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    models.New.objects.filter(new_to_user=user_id).delete()
    chat = models.Chat.objects.filter(Q(send_user=user_id) | Q(to_user=user_id)).order_by('-create_time')
    users = models.Chat.objects.filter(to_user=user_id).values('send_user__username', 'send_user__avatar',
                                                               'send_user_id').distinct()
    reword = models.Chat.objects.filter(send_user=user_id).values('to_user__username', 'to_user__avatar',
                                                                  'to_user_id').distinct()
    strategy = models.Strategy.objects.filter(author=user_id)
    user_collection = models.Strategy.objects.filter(collections=user_id)
    up_count = 0
    collection_count = 0
    fans = models.Follow.objects.filter(follow_id=user_id)
    follow = models.Follow.objects.filter(fan_id=user_id)
    for item in strategy:
        up_count += item.users_like_count
        collection_count += item.collections_count
    return render(request, 'home/chat_page.html', locals())


@csrf_exempt
def del_chat(request):
    user_id = request.session['user_id']
    somebody = request.POST.get('id')
    models.Chat.objects.filter(send_user=user_id, to_user=somebody).delete()
    models.Chat.objects.filter(send_user=somebody, to_user=user_id).delete()
    result = {'status': '删除成功'}
    return JsonResponse(result)


def open_dialog(request, id):
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    another_id = id
    models.New.objects.filter(new_to_user=user_id).delete()
    name = models.User.objects.get(id=another_id).username
    chat_dialog = models.Chat.objects.filter(
        Q(send_user=user_id, to_user=another_id) | Q(to_user=user_id, send_user=another_id)).order_by('-create_time')
    strategy = models.Strategy.objects.filter(author=user_id)
    user_collection = models.Strategy.objects.filter(collections=user_id)
    up_count = 0
    collection_count = 0
    fans = models.Follow.objects.filter(follow_id=user_id)
    follow = models.Follow.objects.filter(fan_id=user_id)
    for item in strategy:
        up_count += item.users_like_count
        collection_count += item.collections_count
    return render(request, 'home/dialog_page.html', locals())


@csrf_exempt
def follow(request):
    follow_user_id = request.POST.get('follow_user_id')
    follow_user = models.User.objects.get(id=follow_user_id)
    fan_user_id = request.session['user_id']
    fan_user = models.User.objects.get(id=fan_user_id)
    new_follow = models.Follow.objects.create(
        follow_id=follow_user_id,
        fan_id=fan_user_id
    )
    new_follow.save()
    result = {'status': '关注成功'}
    return JsonResponse(result)


@csrf_exempt
def unfollow(request):
    follow_user_id = request.POST.get('follow_user_id')
    follow_user = models.User.objects.get(id=follow_user_id)
    fan_user_id = request.session['user_id']
    fan_user = models.User.objects.get(id=fan_user_id)
    del_follow = models.Follow.objects.filter(follow_id=follow_user_id, fan_id=fan_user_id)
    if del_follow:
        del_follow.delete()
    result = {'status': '取消关注'}
    return JsonResponse(result)


@csrf_exempt
def report(request):
    user_id = request.session['user_id']
    user = models.User.objects.get(id=user_id)
    target_id = request.POST.get('target_id')
    target = models.User.objects.get(id=target_id)
    reason = request.POST.get('reason')
    details = request.POST.get('details')
    new_report = models.Report.objects.create(
        target=target,
        report=user,
        reason=reason,
        details=details
    )
    new_report.save()
    result = {'status': '举报成功，管理员将会进行处理！'}
    return JsonResponse(result)
