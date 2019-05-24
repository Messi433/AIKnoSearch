# _*_ coding: utf-8 _*_
__author__ = 'caoke'
__date__ = '2018/12/7'

from django.core.mail import send_mail
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from users.models import EmailVerification
from commons.utils import return_random_str
from AIKnoSearch.settings import EMAIL_FROM

'''邮箱验证码'''


# 邮箱激活账户
def send_email_code(email, type):
    if type == 'register':
        # 随机数类型
        random_type = 'email_link'
        # 随机数
        code = return_random_str(random_type)

        subject = 'AIKnoSearch网站账号激活'
        content = loader.render_to_string(template_name="users/mail/email_register.html").format(code)
        message = EmailMultiAlternatives(subject, content, EMAIL_FROM, [email])
        message.content_subtype = "html"
        message.send()

        email_veri = EmailVerification()
        email_veri.code = code
        email_veri.email = email
        email_veri.type = type
        email_veri.save()

    # 用户密码信息修改
    elif type == 'modify':
        # 随机数类型
        random_type = 'number'
        # 随机数
        code = return_random_str(random_type)

        subject = 'AIKnoSearch用户信息修改'
        content = loader.render_to_string(template_name="users/mail/email_update_password.html").format(code)
        message = EmailMultiAlternatives(subject, content, EMAIL_FROM, [email])
        message.content_subtype = "html"
        message.send()

        try:
            # 取出已有验证码和传入的邮箱对应的对象
            email_veri = EmailVerification.objects.get(Q(email=email) & Q(type=type))
        except Exception as e:
            email_veri = None

        # 如果数据库有该邮箱的验证码执行更新操作否则执行插入操作
        if email_veri:
            email_veri.code = code
            # 若数据库有历史验证码则设置新的验证码为未激活状态
            email_veri.status = 0
            email_veri.save()
        else:
            email_veri = EmailVerification()
            email_veri.code = code
            email_veri.email = email
            email_veri.type = type
            email_veri.save()

    # 用户邮箱信息修改
    elif type == 'update':
        # 随机数类型
        random_type = 'email'
        # 随机数
        code = return_random_str(random_type)

        subject = 'AIKnoSearch用户信息修改'
        content = loader.render_to_string(template_name="users/mail/email_update.html").format(code)
        message = EmailMultiAlternatives(subject, content, EMAIL_FROM, [email])
        message.content_subtype = "html"
        message.send()

        try:
            # 取出已有验证码和传入的邮箱对应的对象
            email_veri = EmailVerification.objects.get(Q(email=email) & Q(type=type))
        except Exception as e:
            email_veri = None

        # 如果数据库有该邮箱的验证码执行更新操作否则执行插入操作
        if email_veri:
            email_veri.code = code
            email_veri.status = 0
            email_veri.save()
        else:
            email_veri = EmailVerification()
            email_veri.code = code
            email_veri.email = email
            email_veri.type = type
            email_veri.save()
    else:
        return "error_code"
