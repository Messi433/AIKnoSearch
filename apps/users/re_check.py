import re


# 验证用户名是否合法
def check_username(str):
    re_match = re.match(r'^[0-9a-zA-z_]{5,12}$', str)
    if re_match:
        return None
    else:
        return "用户名必须是5-12位字母数字、符号、下划线"


# 验证密码及重复密码是否合法
def check_password(str):
    re_match = re.match(r'^(?=.*\d)(?=.*[A-Za-z])[\da-zA-Z!_@#$%^&*()]{8,16}$', str)
    if re_match:
        return None
    else:
        return "密码最少包含1个大写或小写字母、1个数字，长度8到16"


# 验证邮箱是否合法
def check_email(str):
    re_match = re.match(r'^[\w\-]+@[a-z0-9A-Z]+(\.[a-zA-Z]{2,3}){1,2}$', str)
    if re_match:
        return None
    else:
        return "邮箱格式错误"


# 验证邮箱验证码是否合法
def check_email_code(str):
    re_match = re.match(r'^\w{6}$', str)
    if re_match:
        return None
    else:
        return "邮箱验证码为6个字符"

# 图片验证码以及nickname验证已经让django自带form验证过了

