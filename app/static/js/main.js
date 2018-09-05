// 初始化wow.js
new WOW().init();

// ----------------------------------------------------------
// 登录页面 登录页面 登录页面 登录页面 登录页面 登录页面 登录页面 登录页面 登录页面

// 登录页面 默认焦点
$('#login-form').on('shown.bs.modal',function(e){
    $('#login-username').focus();
})

// 收起登录模态框
$('#login-form').on('hidden.bs.modal',function(e){
    // 清空填写信息
    $("#login-form input").val("");
})

// 发起登录请求
$('.login-form').submit(function (e) { 
    e.preventDefault();
    var params = {
        "username": $('#login-username').val(),
        "password": $('#login-password').val(),
    };
    
    $.ajax({
        url: "/login",
        type: "post",
        contentType: "application/json",
        data: JSON.stringify(params),
        success: function (resp) {
            if (resp.errno == "0") {
                // 代表注册成功就代表登录成功
                location.reload();
            } else {
                // 代表注册失败
                alert(resp.errmsg);
                $("#register-password-err").html(resp.errmsg);
                $("#register-password-err").show();
            }
        },
    })
})


// ----------------------------------------------------------
// 注册页面 注册页面 注册页面 注册页面 注册页面 注册页面 注册页面 注册页面 注册页面

// 注册页面 点击输入框的X重置输入框
$('.register-form .glyphicon-remove').click(function(){
    var beClickNamelist = $(this).attr('id').split('-');
    beClickNamelist.pop();
    var beResetId = beClickNamelist.join('-');
    $('#'+beResetId).val('');
    $('#'+beResetId).focus();
    $('#register-error').html('');
})

// 打开注册模态框
$('#register-form').on('shown.bs.modal',function(e){
    // 默认焦点
    $('#username').focus();
    // 刷新验证码
    $('#img-idcode-display').html(idcodeRandom());
})

// 收起注册模态框
$('#register-form').on('hidden.bs.modal',function(e){
    // 清空填写信息
    $("#register-form input").val("");
    // 隐藏判断span
    $('#register-form .form-control-feedback').hide();
    // 
    for (x in checks){
        checks[x][1] = false;
    }
})

// 注册页面 点击验证码
$('#img-idcode-display').click(function (e) { 
    e.preventDefault();
    // 刷新验证码
    $(this).html(idcodeRandom());
    // 焦点调整到填写验证码
    $('#img-idcode').focus();
})

// 定义手机校验码变量
var phoneIdcode;

// 生成四位随机验证码
var randWord;
function idcodeRandom(){
    var letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '@', '%', '&', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    randWord =  
        letters[Math.floor(Math.random() * 30)] +
        letters[Math.floor(Math.random() * 39)] +
        letters[Math.floor(Math.random() * 39)] +
        letters[Math.floor(Math.random() * 39)];
    return randWord;
}

// 所有数据变量校验值
var checks = {
    'username':[
        // 校验函数
        function(v){
            var reg = /^[\D][\u4e00-\u9fff\w]{1,10}$/;
            return reg.test(v);
        },
        // 校验结果
        false,
        // 校验成功后的数据
        '',
        // 校验错误信息
        '用户名:2-11位(中文、字母、数字、下划线)/非数字开头',
    ],
    'password':[
        function(v){
            var reg = /[a-zA-Z0-9~!@#%&=;':",./<>_\-\}\]\$\(\)\*\+\.\[\?\\\^\{\|]{6,20}$/;
            return reg.test(v);
        },
        false,
        '',
        '密码需6-20位',
    ],
    'confirm-password':[
        function(v){
            return v == $('#password').val() && v != ''
        },
        false,
        '',
        '两次密码输入不一致',
    ],
    'img-idcode':[
        function(v){
            return v == randWord;
        },
        false,
        '',
        '请输入正确的验证码',
    ],
    'phone-num':[
        function(v){
            var reg = /^[0-9]{11}$/;
            return reg.test(v);
        },
        false,
        '',
        '手机号码只能为11位数字',
    ],
    'phone-idcode':[
        function(v){
            return v == phoneIdcode;
        },
        false,
        '',
        '请输入正确的验证码',
    ],
}

// 注册页面 所有输入校验
$('#register-form input').blur(function (e) { 
    e.preventDefault();
    var idName = $(this).attr('id');
    var value = $(this).val();
    var check = checks[idName][0](value);
    if (check){
        $('#'+idName+'-ok').show();
        $('#'+idName+'-no').hide();
        $('#register-error').html('');
        checks[idName][1] = true;
        checks[idName][2] = value;
    }else{
        $('#'+idName+'-no').show();
        $('#'+idName+'-ok').hide();
        $('#register-error').html(checks[idName][3]);
        $('#register-error').show();
    }
})

// 注册页面 获取短信验证码
$('#get-phone-idcode').click(function (e) { 
    e.preventDefault();
    if (!checks['phone-num'][1]){
        alert('请输入正确的手机号');
        return;
    }

    var checksList = ['username','password','confirm-password','img-idcode','phone-num']
    for (x in checksList){
        if (!checks[checksList[x]][1]){
            alert($('label[for="'+ checksList[x] +'"]').text()+'格式错误');
            return;
        }
    }

    $(this).removeClass('btn-primary').addClass('disabled');
    $(this).html('<span id="phone-idcode-loading-num">59</span> 秒后重新获取');
    $('#phone-idcode-loading-num').css('corlor','red');
    var loadingNum = $('#phone-idcode-loading-num').text();
    var loadingTimer = setInterval(function(){
        loadingNum--;
        $('#phone-idcode-loading-num').html(loadingNum);
        if (loadingNum == 0) {
            clearInterval(loadingTimer);
            $('#get-phone-idcode').html('重新获取校验码');
            $('#get-phone-idcode').removeClass('disabled').addClass('btn-primary');
            checks['phone-idcode'][1] = false;
        }
    },1000)


    // 发起请求验证码的请求
    var params = {
        "mobile": checks['phone-num'][2],
    }

    $.ajax({
        url: "/get_phone_idcode",
        type: "post",
        contentType: "application/json",
        data: JSON.stringify(params),
        success: function (resp) {
            if (resp.errno == "0") {
                phoneIdcode = resp.idCode;
            } else {
                clearInterval(loadingTimer);
                $('#phone-num-no').show();
                $('#phone-num-ok').hide();
                $('#get-phone-idcode').html('获取短信校验码');
                $('#get-phone-idcode').removeClass('disabled').addClass('btn-primary');
                alert(resp.errmsg);
            }
        },
    })
})

$('.register-form').submit(function (e) { 
    e.preventDefault();
    // 校验表单所有输入布尔值
    for (x in checks){
        if (!checks[x][1]){
            alert($('label[for="'+ x +'"]').text()+'格式错误');
            return;
        }
    }

    // 发起注册请求
    var params = {
        "username": $('#username').val(),
        "password": $('#password').val(),
        "mobile": $('#phone-num').val(),
    }

        $.ajax({
            url: "/register",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(params),
            success: function (resp) {
                if (resp.errno == "0") {
                    // 代表注册成功就代表登录成功
                    location.reload();
                } else {
                    // 代表注册失败
                    alert(resp.errmsg);
                    $("#register-password-err").html(resp.errmsg);
                    $("#register-password-err").show();
                }
            }
        })
})
