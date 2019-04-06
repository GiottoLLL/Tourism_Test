# -*- coding: utf-8 -*-
# @Time    : 2019/4/5 2:46
# @Author  : GiottoLLL
# @Email   : GiottoLLL7@gmail.com
# @File    : form.py
# @Software: PyCharm
from django import forms
from captcha.fields import CaptchaField


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
    captcha = CaptchaField(label='验证码')
