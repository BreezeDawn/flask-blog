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
        letters[Math.floor(Math.random() * 39)]
    return randWord
}

// 注册页面 注册页面 注册页面 注册页面 注册页面 注册页面 注册页面 注册页面 注册页面

// 所有数据变量校验值
var checks = {
    'username':[
        function(v){
            var reg = /^[\D]{2,11}$/;
            return reg.test(v)
        },
        false,
    ],
    'password':[
        function(v){
            var reg = /[a-zA-Z0-9~!@#%&=;':",./<>_\-\}\]\$\(\)\*\+\.\[\?\\\^\{\|]{6,20}$/;
            return reg.test(v)
        },
        false,
    ],
    'confirm-password':[
        function(v){
            return v == $('#password').val() && v != ''
        },
        false,
    ],
    'img-idcode':[
        function(v){
            return v == randWord
        },
        false,
    ],
    'phone-num':[
        function(v){
            var reg = /^[0-9]{11}$/;
            return reg.test(v)
        },
        false,
    ],
    'phone-idcode':[
        function(v){
            return v == phoneIdcode
        },
        false
    ],
}


// 注册页面 验证码的显示
$('.register').click(function (e) { 
    e.preventDefault();
    $('#img-idcode-display').html(idcodeRandom())
});

// 注册页面 默认焦点
$('#register-form').on('shown.bs.modal',function(e){
    $('#username').focus();
});

// 注册页面 点击验证码 刷新验证码
$('#img-idcode-display').click(function (e) { 
    e.preventDefault();
    $(this).html(idcodeRandom())
    $('#img-idcode').focus();
});

// 注册页面 所有输入校验
$('form input').blur(function (e) { 
    e.preventDefault();
    var idName = $(this).attr('id')
    var value = $(this).val();
    var check = checks[idName][0](value)
    if (check){
        $('#'+idName+'-ok').show();
        $('#'+idName+'-no').hide();
        $('#'+idName+'-error').hide();
        checks[idName][1] = true
        checks[idName][2] = value
    }else{
        $('#'+idName+'-no').show();
        $('#'+idName+'-ok').hide();
        $('#'+idName+'-error').show();
    };
});

// 注册页面 获取短信验证码
$('#get-phone-idcode').click(function (e) { 
    e.preventDefault();
    if (!checks['phone-num'][1]){
        $('#phone-idcode-error').html('请输入手机号');
        $('#phone-idcode-error').show();
        return
    }
    $(this).removeClass('btn-primary').addClass('disabled');
    $(this).html('<span id="phone-idcode-loading-num">59</span> 秒后重新获取');
    $('#phone-idcode-loading-num').css('corlor','red')
    var loadingNum = $('#phone-idcode-loading-num').text();
    var loadingTimer = setInterval(function(){
        loadingNum--;
        $('#phone-idcode-loading-num').html(loadingNum);
        if (loadingNum == 0) {
            clearInterval(loadingTimer);
            $('#get-phone-idcode').html('重新获取校验码');
            $('#get-phone-idcode').removeClass('disabled').addClass('btn-primary');
            $('#phone-idcode-error').html('验证码已过期');
            $('#phone-idcode-error').show();
            checks['phone-idcode'][1] = false;
        }
    },1000)


    // 发起请求验证码的请求
    var params = {
        "mobile": checks['phone-num'][2]
    }

    $.ajax({
        url: "/get_phone_idcode",
        type: "post",
        contentType: "application/json",
        data: JSON.stringify(params),
        success: function (resp) {
            if (resp.errno == "0") {
                phoneIdcode = resp.idCode
            } else {
                clearInterval(loadingTimer);
                $('#phone-num-no').show();
                $('#phone-num-ok').hide();
                $('#get-phone-idcode').html('获取短信校验码');
                $('#get-phone-idcode').removeClass('disabled').addClass('btn-primary');
                alert(resp.errmsg)
            }
        }
    });
});

$('.register-form').submit(function (e) { 
    e.preventDefault();
    // 校验表单所有输入布尔值
    for (x in checks){
        if (!checks[x][1]){
            alert($('label[for="'+ x +'"]').text()+'格式错误')
            return
        }
    }

    // 发起注册请求
    var params = {
        "username": $('#username').val(),
        "password": $('#password').val(),
        "mobile": $('#phone-num').val()
    }

        $.ajax({
            url: "/register",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(params),
            success: function (resp) {
                if (resp.errno == "0") {
                    // 代表注册成功就代表登录成功
                    location.reload()
                } else {
                    // 代表注册失败
                    alert(resp.errmsg)
                    $("#register-password-err").html(resp.errmsg)
                    $("#register-password-err").show()
                }
            }
        })
});