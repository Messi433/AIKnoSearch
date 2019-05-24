# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/12/1'

from django import forms
from captcha.fields import CaptchaField


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': u"用户名不能为空"})
    password = forms.CharField(required=True, min_length=8,
                               error_messages={'required': u"密码不能为空", 'min_length': u"密码至少为8个字符"})


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(required=False,max_length=10,error_messages={'max_length': u"昵称最多为10个字符"})
    username = forms.CharField(required=True, min_length=5,max_length=12,
                               error_messages={'required': u"用户名不能为空", 'min_length': u"用户名至少为5个字符",
                                               'max_length': u"用户名最多为12个字符"})
    password = forms.CharField(required=True, min_length=8,max_length=16,
                               error_messages={'required': u"密码不能为空", 'min_length': u"密码至少为8个字符",
                                               'max_length': u"密码最多为16个字符"})
    captcha = CaptchaField(required=True, error_messages={'required': u"验证码不能为空", 'invalid': u"验证码错误"})


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8,max_length=16,
                               error_messages={'required': u"密码不能为空", 'min_length': u"密码至少为8个字符",
                                               'max_length': u"密码最多为16个字符"})
    captcha = CaptchaField(required=True, error_messages={'required': u"验证码不能为空", 'invalid': u"验证码错误"})
    email_code = forms.CharField(required=True, min_length=6,
                                 error_messages={'required': u"邮箱验证码不能为空", 'min_length': u"邮箱验证码为6个字符"})


class SendEmailForm(forms.Form):
    email = forms.EmailField(required=True)


class ResetEmailForm(forms.Form):
    pass
