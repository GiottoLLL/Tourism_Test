# -*- coding: utf-8 -*-
# @Time    : 2019/4/5 2:46
# @Author  : GiottoLLL
# @Email   : GiottoLLL7@gmail.com
# @File    : form.py
# @Software: PyCharm
from django import forms
from captcha.fields import CaptchaField
from ckeditor_uploader.fields import RichTextUploadingFormField
from .models import Tags


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': "用户名"}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'Input', 'placeholder': "密码"}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, initial='用户名',
                               widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': "用户名"}))
    password1 = forms.CharField(label="密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'Input', 'placeholder': "密码"}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'Input', 'placeholder': "确认密码"}))
    phone = forms.IntegerField(label="手机号", widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': "手机号"}))
    sex = forms.ChoiceField(label='性别', choices=gender)


class WriteForm(forms.Form):
    title = forms.CharField(label="标题", max_length=50,
                            widget=forms.TextInput(attrs={'class': 'title-input', 'placeholder': "请输入标题（最多50个字）"}))
    content = RichTextUploadingFormField(label='内容')
    img = forms.ImageField(widget=forms.FileInput(attrs={'style': 'display:none'}))


class CommentForm(forms.Form):
    content = forms.CharField(label="评论", widget=forms.TextInput(attrs={'class': 'input-content'}))
    strategy = forms.CharField(label="攻略", widget=forms.TextInput(attrs={'class': 'hide-strategy'}))
    to_someone = forms.CharField(label="回复", widget=forms.TextInput(attrs={'class': 'hide-author'}))


class ReportForm(forms.Form):
    item = (
        ('spam', '垃圾信息'),
        ('unfriendly', '不友善信息'),
        ('harm', '有害信息'),
        ('tort', '涉嫌侵权'),
        ('other', '其他'),
    )
    reason = forms.ChoiceField(label="理由", choices=item)
    details = forms.CharField(label="详情", widget=forms.Textarea(attrs={'class': 'textarea'}))
