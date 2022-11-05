function alertTips() {
    alert('成功跳转');
}

function show_login(){
    window.location.href = '/login/';
}

function show_regist(){
    window.location.href = '/regist/';
}

function sendPostJson_login() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
        xmlhttp = new XMLHttpRequest();
    } else {
        // IE6, IE5 浏览器执行代码
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    // 获取输入框的值
    var Username = document.getElementById("username").value;
    var Password = document.getElementById("password").value;
    // 发送POST-JSON请求
    xmlhttp.open("POST", "/api/login/", true);  //login接口
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send(JSON.stringify({"username": Username, "password": Password}));
    //请求后的回调接口，可将请求成功后要执行的程序写在其中
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {//验证请求是否发送成功
            var json = xmlhttp.responseText;  //获取到服务端返回的数据
            json = JSON.parse(json);
            if (json['code'] == 201) {
                window.location.href = "/home/"; //跳转主页连接
            } else if(json['code'] == 422) {
                alert('用户名或密码错误!');
                window.location.href = "/login/"; //重新跳转连接
            }
        }
    }
}

$(function () {
    $('form').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            username: {
                message: '用户名验证失败',
                validators: {
                    notEmpty: {
                        message: '用户名不能为空'
                    },
                    stringLength: {
                        min: 4,
                        max: 18,
                        message: '用户名长度不能小于4位'
                    },
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: '密码不能为空'
                    },
                    stringLength: {
                        min: 8,
                        max: 18,
                        message: '密码长度不能小于8位'
                    },
                }
            },
            mail: {
                validators: {
                    notEmpty: {
                        message: '邮箱不能为空'
                    },
                    stringLength: {
                        min: 7,
                        max: 18,
                        message: '邮箱长度不能小于7位'
                    },
                }
            },
        }
    });
});