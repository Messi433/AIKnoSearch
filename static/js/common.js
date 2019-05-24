var index_url = '/';
var login_url = '/login/';
var suggest_url = '/suggest/';
var search_url = '/search/';
var verify_url = '/verify/';
clear_history_url = '/clear_history/';

/*登录操作*/
function commonLogin() {
    //关闭异步
    /*$.ajaxSetup({
        async: false
    });*/
    //关闭模态窗口清空错误提示和输入框内容
    $('.login-cancel').click(function () {
        $('.error-login-div').hide();
        $('.error-login-msg').text('');
        $('.login-input').val('');
        $('.login-input').removeClass('warning');
    });
    //输入框获得焦点时清空错误提示
    $("input[name = 'login-username']").focus(function () { //获取焦点
        $(this).val("");
        //清空错误提示
        $('.error-login-div').hide();
        $('.error-login-msg').text('');
        $('.login-input').removeClass('warning')
    });
    $("input[name = 'login-password']").focus(function () { //获取焦点
        $(this).val("");
        //清空错误提示
        $('.error-login-div').hide();
        $('.error-login-msg').text('');
        $('.login-input').removeClass('warning')
    });
    //登录字段验证
    //按钮提交
    $('.login-submit').on('click', function () {
        //错误提示清空
        $('.error-login-div').hide();
        $('.error-login-msg').text('');
        var username = $('.login-username').val();
        var password = $('.login-password').val();
        if (username.length === 0) {
            $('.login-username').addClass('warning');
            $('.error-login-div').show();
            $('.error-login-msg').text('请输入用户名或邮箱');
        } else if (password.length === 0) {
            $('.login-password').addClass('warning');
            $('.error-login-div').show();
            $('.error-login-msg').text('请输入密码');
        }
        if (username.length === 0 || password.length === 0) {
            //表单禁止提交
            $('.login-form').submit(function () {
                return false;
            });
        } else {
            //ajax实现登录验证
            $.ajax({
                cache: false,
                type: 'POST',
                data: {
                    username, password
                },
                dataType: 'json',
                url: login_url,
                async: false,
                success: function (data) {
                    if (data.status == 'success') {
                        //跳转首页
                        window.location.href = index_url;
                    } else if (data.status == 'fail') {
                        console.log(data.msg)
                        //错误信息提示
                        $('.error-login-div').show();
                        $('.error-login-msg').text(data.msg);
                    }
                },
                error: function (data) {
                    console.log("ajax error");
                }
            });
        }
    });
}

/*表单验证*/

/*
* 获得或失去输入框焦点时的函数
* */

//注册
function checkRegFocus() {
    $("input[name='username']").blur(checkUsername);
    $("input[name = 'username']").focus(function () { //获取焦点
        // $(this).val("");
        //清空错误提示
        $(this).parent().next().html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });
    $("input[name='nickname']").blur(checkNickname);
    $("input[name = 'nickname']").focus(function () { //获取焦点
        $(this).parent().next().html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });
    $("input[name='password']").blur(checkPassword);
    $("input[name='password']").focus(function () {
        $(this).parent().next().html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });
    $("input[name='repassword']").blur(checkRepassword);
    $("input[name='repassword']").focus(function () {
        $(this).parent().next().html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });
    $("input[name='email']").blur(checkEmail);
    $("input[name='email']").focus(function () {
        $(this).parent().next().html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });
    $("input[name='captcha_1']").blur(checkCaptcha);
    $("input[name='captcha_1']").focus(function () {
        $(".captcha-span").html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });
}

//账户信息重置
function checkResetFocus() {
    $("input[name='email']").blur(checkEmail);
    $("input[name='email']").focus(function () {
        $(this).parent().next().html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });
    $("input[name='password']").blur(checkPassword);
    $("input[name='password']").focus(function () {
        $(this).parent().next().html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });
    $("input[name='repassword']").blur(checkRepassword);
    $("input[name='repassword']").focus(function () {
        $(this).parent().next().html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });
    $("input[name='email_code']").blur(checkEmailCode);
    $("input[name='email_code']").focus(function () {
        $(".email-code-span").html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });
    $("input[name='captcha_1']").blur(checkCaptcha);
    $("input[name='captcha_1']").focus(function () {
        $(".captcha-span").html("");
        $('.errorlist').hide();
        $('.msg-div').hide();
    });

}

// 用户名验证
function checkUsername() {
    var username = $('#username').val();
    var regstr = /^[0-9a-zA-z_]{5,12}$/;
    if (username.length == 0) {
        $('#username').parent().next().html("请输入用户名").css("color", "red");
        return false;
    } else if (!regstr.test(username)) {
        $('#username').parent().next().html("用户名必须是5-12位字母数字、符号、下划线").css("color", "red");
        return false;
    }
    return true;
}

// 昵称验证
function checkNickname() {
    var nickname = $("#nickname").val();
    if (nickname.length > 10) {
        $(this).parent().next().html("昵称不能超过5个汉字或10个字符").css("color", "red");
        return false;
    }
    return true;
}

// 密码及重复密码验证
function checkPassword() {
    var password = $("#password").val();
    var regstr = /^(?=.*\d)(?=.*[A-Za-z])[\da-zA-Z!@#$%^&*_()]{8,16}$/;
    if (password.length == 0) {
        $("#password").parent().next().html("请输入密码").css("color", "red");
        return false;
    } else if (!regstr.test(password)) {
        $("#password").parent().next().html("密码最少包含1个大写或小写字母、1个数字，长度8到16").css("color", "red");
        return false;
    }
    return true;
}

function checkRepassword() {
    var repassword = $('#repassword').val();//重复密码
    var password = $('#password').val();//密码
    if (repassword.length == 0) {
        $('#repassword').parent().next().html("请输入密码").css("color", "red");
        return false;
    } else if (password != repassword) {
        $('#repassword').parent().next().html("两次密码不一致").css("color", "red");
        return false;
    }
    return true;
}

//邮箱格式验证
function checkEmail() {
    var email = $('#email').val();
    var regstr = /^[\w\-]+@[a-z0-9A-Z]+(\.[a-zA-Z]{2,3}){1,2}$/;
    if (email.length == 0) {
        $('#email').parent().next().html("请输入邮箱账号").css("color", "red");
        return false;
    } else if (!regstr.test(email)) {
        $('#email').parent().next().html("邮箱格式不正确").css("color", "red");
        return false;
    }
    return true;
}

//验证码判断是否为空
function checkCaptcha() {
    var captcha = $("#id_captcha_1").val();
    if (captcha.length == 0) {
        $(".captcha-span").html("请输入验证码");
        return false;
    }
    return true;

}

//邮箱验证码判断是否为空
function checkEmailCode() {
    var emailCode = $("#email_code").val();
    var regstr = /^\w{6}$/;
    if (emailCode.length == 0) {
        $(".email-code-span").html("请输入邮箱验证码");
        return false;
    } else if (!regstr.test(emailCode)) {
        $(".email-code-span").html("邮箱验证码为6个字符");
        return false;
    }
    return true;
}

/*密码重置操作*/

//发送验证码验证
function EmailVeri() {
    $('.email-code-btn').on('click', function () {
        var email = $('#email').val();
        if (checkEmail()) {
            settime(this);
        }
        $.ajax({
            cache: false,
            type: 'POST',
            data: {
                email
            },
            dataType: 'json',
            url: verify_url,
            async: true,
            success: function (data) {
                if (data.status == 'success') {
                    // $('.code-btn-word').html('重新发送(<span class="code-btn-time"></span>)');
                    //倒计时60秒
                    // back(60);
                } else if (data.status == 'fail') {
                    alert("验证码获取错误")
                    console.log(data.msg)
                    //错误信息提示
                    $('.error-div').show();
                    $('.error-msg').text(data.msg);
                }
            },
            error: function (data) {
                console.log("ajax error");
            }
        });
    });
}

//验证码倒计时
var countdown = 60;

function settime(val) {
    if (countdown == 0) {
        val.removeAttribute("disabled");
        val.value = "获取验证码";
        countdown = 60;
    } else {
        val.setAttribute("disabled", true);
        val.value = "重新发送(" + countdown + ")";
        countdown--;
        setTimeout(function () {
            settime(val)
        }, 1000)
    }

}