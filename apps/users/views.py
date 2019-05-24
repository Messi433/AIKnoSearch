import json
import time
import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, render_to_response
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from captcha.views import CaptchaStore, captcha_image_url
import redis

from .models import UserProfile, EmailVerification
from .forms import UserLoginForm, RegisterForm, ResetPasswordForm, SendEmailForm
from .re_check import *
from commons.veri_code import send_email_code
from commons.utils import email_login_access
from commons.commons import delete_redis_key

'''创建redis连接'''
r = redis.StrictRedis(host='localhost', password="k753951", decode_responses=True)


# settings.py配置该类
class CustomBackend(ModelBackend):
    '''自定义authenticate()逻辑'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 获取数据库用户对象
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户登录
class UserLogin(View):

    def post(self, request):
        login_form = UserLoginForm(request.POST)
        '''form验证,判断用户、密码是否为空，密码位数是否合法'''
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            '''调用django authenticate方法进行登录验证(默认账号密码验证),
               邮箱密码验证(需要自定义authenticate())'''
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # 调用django login方法进行登录
                    login(request, user)
                    return HttpResponse(json.dumps({'status': "success", 'msg': {}}),
                                        content_type="application/json")
                else:
                    return HttpResponse(json.dumps({'status': "fail", 'msg': '该账号还未激活'}),
                                        content_type="application/json")
            else:
                return HttpResponse(json.dumps({'status': "fail", 'msg': '用户名或密码错误!'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': "fail", 'msg': login_form}), content_type="application/json")


# 用户登出
class UserLogout(View):
    def get(self, request):
        username = request.user.username
        # 删除用户redis缓存数据
        delete_redis_key(username)
        logout(request)
        return redirect(reverse('index'))


# 用户注册
class Register(View):
    def get(self, request):
        # 验证码参数
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        register_form = RegisterForm()
        return render(request, 'users/register.html', locals())

    def post(self, request):
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            email = request.POST.get('email', "")
            nickname = request.POST.get('nickname', "")
            # 正则表单验证
            username_msg = check_username(username)
            password_msg = check_password(password)
            email_msg = check_email(email)
            re_msgs = []
            if username_msg:
                re_msgs.append(username_msg)
            if password_msg:
                re_msgs.append(password_msg)
            if email_msg:
                re_msgs.append(email_msg)
            if len(re_msgs) > 0:
                return render(request, 'users/register.html', locals())

            # 处理数据库中未激活的用户
            self.delete_inactive_user()

            if UserProfile.objects.filter(username=username):
                msg = "该用户已注册"
                return render(request, 'users/register.html', locals())
            elif UserProfile.objects.filter(email=email):
                msg = "该邮箱已注册"
                return render(request, 'users/register.html', locals())
            elif UserProfile.objects.filter(nickname=nickname):
                msg = "该昵称已存在:)"
                return render(request, 'users/register.html', locals())

            user = UserProfile()
            user.username = username
            # 明文加密
            user.password = make_password(password)
            user.email = email
            user.nickname = nickname
            # 用户状态默认未激活
            user.is_active = False
            user.save()

            # 邮件发送处理
            send_email_code(email, "register")
            # 邮件登录入口
            email_access = email_login_access(email)

            return render(request, "users/activate.html", {"email": email, "email_access": email_access})
        else:
            return render(request, 'users/register.html', locals())

    # 时间差计算(秒)
    def calculate_delta_time(self, date_time):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
        now_time_strip = time.mktime(time.strptime(now_time, "%Y-%m-%d %H:%M:%S"))
        datetime_strip = time.mktime(time.strptime(date_time, "%Y-%m-%d %H:%M:%S"))
        delta_timestrip = now_time_strip - datetime_strip
        return delta_timestrip

    # 删除超时为注册激活用户
    def delete_inactive_user(self):
        users = UserProfile.objects.all()
        for user in users:
            user_is_active = user.is_active
            # 如果用户未激活
            if user_is_active == False:
                user_date_time = user.date_joined
                # 如果用户未激活，且在数据库中存在时间>900s == 15min
                if self.calculate_delta_time(user_date_time) > 900.0:
                    # 删除用户及用户信息
                    EmailVerification.objects.get(email=user.email).delete()
                    user.delete()



# 用户激活账号
class UserActivation(View):
    def get(self, request, activate_code):
        # 返回对应验证链接的对象,链接是随机的所以有可能是重复的,//这是类方法所以直接通过类来查询
        try:
            veri_obj = EmailVerification.objects.get(Q(code=activate_code) & Q(type='register'))
        except Exception as e:
            veri_obj = None
        if veri_obj:
            # 返回验证链接对象对应的邮箱
            veri_email = veri_obj.email
            user = UserProfile.objects.get(email=veri_email)
            if user:
                if user:
                    if user.is_active == True:
                        return render(request, 'users/already_activated.html')
                    else:
                        # 激活状态为True
                        user.is_active = True
                        user.save()
                        veri_obj.status = 1
                        veri_obj.save()
                        return render(request, 'users/register_success.html', {'msg': '注册成功'})
        else:
            return render(request, 'users/error_activated.html')


# 用户重置密码
class ResetPassword(View):
    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'users/reset.html', locals())

    def post(self, request):
        reset_form = ResetPasswordForm(request.POST)
        # 验证码参数
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        reset_form = ResetPasswordForm()
        if reset_form.is_valid():
            # 表单
            email = request.POST.get('email', "")
            password = request.POST.get("password", "")
            email_code = request.POST.get("email_code", "")
            # 正则表单验证
            email_msg = check_email(email)
            password_msg = check_password(password)
            email_code_msg = check_email_code(email_code)
            re_msgs = []
            if email_msg:
                re_msgs.append(email_msg)
            if password_msg:
                re_msgs.append(password_msg)
            if email_code_msg:
                re_msgs.append(email_code_msg)
            if len(re_msgs) > 0:
                return render(request, 'users/reset.html', {locals()})
            try:
                # 取出验证邮箱对应的用户对象
                user = UserProfile.objects.get(email=email)
            except Exception as e:
                user = None
            try:
                # 取出验证码对应的验证邮箱对象
                user_veri = EmailVerification.objects.get(Q(code=email_code) & Q(type="modify"))
            except Exception as e:
                user_veri = None

            if user:
                if user_veri:
                    user_veri_status = user_veri.status
                    if user_veri_status == 0:
                        user.password = make_password(password)
                        user.save()
                        user_veri.status = 1
                        user_veri.save()
                        return render(request, 'users/reset_success.html', locals())
                    elif user_veri_status == 1:
                        msg = '该邮箱验证码已激活'
                        return render(request, 'users/reset.html', locals())
                    else:
                        msg = '未知错误'
                        return render(request, 'users/reset.html', locals())
                else:
                    msg = '邮箱验证码错误'
                    return render(request, 'users/reset.html', locals())
            else:
                msg = '邮箱不存在'
                return render(request, 'users/reset.html', locals())
        else:
            return render(request, 'users/reset.html', locals())


class EmailVeriCode(View):
    def post(self, request):
        send_email_form = SendEmailForm(request.POST)
        if send_email_form.is_valid():
            email = request.POST.get("email", "")
            send_email_code(email, 'modify')
            return HttpResponse(json.dumps({'status': "success", 'msg': {}}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': "success", 'msg': send_email_form}),
                                content_type="application/json")


# 用户账号注销bug
class UserCancellation(View):
    def get(self, request):
        pass


# 404处理
def page_not_found(request):
    resp = render_to_response("404.html", {})
    resp.status_code = 404
    return resp


# 500处理
def server_error(request):
    resp = render_to_response("500.html", {})
    resp.status_code = 500
    return resp


# 403处理
def permission_denied(request):
    resp = render_to_response("403.html", {})
    resp.status_code = 403
    return resp
