var maxround;
var epsilon;
var aggregationtiming;
var batchsize;
var lr;
var token;
var client_num=1;
var max_num=100;

function sleep(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function alertTips() {
    swal("成功跳转！","","success");
}

function logout() {
    document.getElementById('token').value = null;
    window.location.href = "/login/";
}

function show_home() {
    document.getElementById("tasklist").style.backgroundColor = "midnightblue";
    document.getElementById("home").style.backgroundColor = "lightblue";
    document.getElementById("infolist").style.backgroundColor = "midnightblue";
    document.getElementById("user").style.backgroundColor = "midnightblue";
    document.getElementById("home_box").style.display = "block";
    document.getElementById("tasklist_box").style.display = "none";
    document.getElementById("strategy").style.display = "none";
    document.getElementById("info_box").style.display = "none";
    document.getElementById("user_box").style.display = "none";
    document.getElementById("detail_box").style.display = "none";
    document.getElementById("deploy_task").style.display = "none";
    document.getElementById("create_task").style.display = "none";
    document.getElementById("home_box").style.opacity = "1";
}

function show_tasklist() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
        xmlhttp = new XMLHttpRequest();
    } else {
        // IE6, IE5 浏览器执行代码
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    var Token = document.getElementById('token').innerHTML;
    xmlhttp.open("POST", "/api/task_visualize/", true);  //home主页接口
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send(JSON.stringify({"token": Token}));
    xmlhttp.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {//验证请求是否发送成功
            var json = xmlhttp.responseText;  //获取到服务端返回的数
            json = JSON.parse(json);
            var servicename = json['data']['servicename'];
            var servicebrief = json['data']['servicebrief'];
            var servicedetail = json['data']['servicedetail'];
            maxround = json['data']['strategies']['maxround'];
            aggregationtiming = json['data']['strategies']['aggregationtiming'];
            epsilon = json['data']['strategies']['epsilon'];
            batchsize = json['data']['strategies']['batchsize'];
            lr = json['data']['strategies']['lr'];
            if (json['code'] == 200) {
                document.getElementById('servicename1').value=servicename;
                document.getElementById('servicebrief1').value=servicebrief;
                document.getElementById('servicedetail1').value=servicedetail;
                document.getElementById('servicename2').value="Service2";
                document.getElementById('servicebrief2').value="trainable";
                document.getElementById('servicedetail2').value="Service2 able to be trained";
                document.getElementById('maxround').value = window.maxround;
                document.getElementById('aggregationtiming').value = window.aggregationtiming;
                document.getElementById('epsilon').value = window.epsilon;
                document.getElementById('batchsize').value = window.batchsize;
                document.getElementById('lr').value = window.lr;
            } else if(json['code'] == 400) {
                swal("请求任务列表失败!","","warning");
                window.location.href = "/login/"; //跳转任务列表界面连接
            }
        }
    }
    document.getElementById("tasklist").style.backgroundColor = "lightblue";
    document.getElementById("home").style.backgroundColor = "midnightblue";
    document.getElementById("infolist").style.backgroundColor = "midnightblue";
    document.getElementById("user").style.backgroundColor = "midnightblue";
    document.getElementById("home_box").style.display = "none";
    document.getElementById("tasklist_box").style.display = "block";
    document.getElementById("tasklist_box").style.opacity = "1";
    document.getElementById("strategy").style.display = "none";
    document.getElementById("info_box").style.display = "none";
    document.getElementById("user_box").style.display = "none";
    document.getElementById("detail_box").style.display = "none";
    document.getElementById("deploy_task").style.display = "none";
    document.getElementById("create_task").style.display = "none";
}

function show_infolist() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
        xmlhttp = new XMLHttpRequest();
    } else {
        // IE6, IE5 浏览器执行代码
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    var Token = document.getElementById('token').innerHTML;
    xmlhttp.open("POST", "/api/info_visualize/", true);  //home主页接口
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send(JSON.stringify({"token": Token}));
    xmlhttp.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {//验证请求是否发送成功
            var json = xmlhttp.responseText;  //获取到服务端返回的数
            json = JSON.parse(json);
            if (json['code'] == 200) {
                document.getElementById("message").value = json['message'];
                document.getElementById("tasklist").style.backgroundColor = "midnightblue";
                document.getElementById("home").style.backgroundColor = "midnightblue";
                document.getElementById("infolist").style.backgroundColor = "lightblue";
                document.getElementById("user").style.backgroundColor = "midnightblue";
                document.getElementById("home_box").style.display = "none";
                document.getElementById("tasklist_box").style.display = "none";
                document.getElementById("strategy").style.display = "none";
                document.getElementById("info_box").style.display = "block";
                document.getElementById("user_box").style.display = "none";
                document.getElementById("detail_box").style.display = "none";
                document.getElementById("deploy_task").style.display = "none";
                document.getElementById("create_task").style.display = "none";
                document.getElementById("info_box").style.opacity = "1";
            } else if(json['code'] == 400) {
                swal("请求任务列表失败!","","warning");
                window.location.href = "/login/"; //跳转任务列表界面连接
            }
        }
    }
}

function show_userpage() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
        xmlhttp = new XMLHttpRequest();
    } else {
        // IE6, IE5 浏览器执行代码
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    var Token = document.getElementById('token').innerHTML;
    xmlhttp.open("POST", "/api/userpage_source/", true);  //home主页接口
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send(JSON.stringify({"token": Token}));
    xmlhttp.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {//验证请求是否发送成功
            var json = xmlhttp.responseText;  //获取到服务端返回的数
            json = JSON.parse(json);
            if (json['code'] == 200) {
                document.getElementById("tasklist").style.backgroundColor = "midnightblue";
                document.getElementById("home").style.backgroundColor = "midnightblue";
                document.getElementById("infolist").style.backgroundColor = "midnightblue";
                document.getElementById("user").style.backgroundColor = "lightblue";
                document.getElementById("home_box").style.display = "none";
                document.getElementById("tasklist_box").style.display = "none";
                document.getElementById("strategy").style.display = "none";
                document.getElementById("info_box").style.display = "none";
                document.getElementById("user_box").style.display = "block";
                document.getElementById("detail_box").style.display = "none";
                document.getElementById("deploy_task").style.display = "none";
                document.getElementById("create_task").style.display = "none";
                document.getElementById("user_box").style.opacity = "1";
            } else if(json['code'] == 400) {
                swal("请求任务列表失败!","","warning");
                window.location.href = "/login/"; //跳转任务列表界面连接
            }
        }
    }
}

function show_tasklist_window() {
    document.getElementById("tasklist_box").style.opacity = "0.2";
    document.getElementById("strategy").style.display = "block";
}

function close_tasklist_window() {
    document.getElementById("tasklist_box").style.opacity = "1";
    document.getElementById("strategy").style.display = "none";
    document.getElementById('maxround').value = window.maxround;
    document.getElementById('aggregationtiming').value = window.aggregationtiming;
    document.getElementById('epsilon').value = window.epsilon;
    document.getElementById('batchsize').value = window.batchsize;
    document.getElementById('lr').value = window.lr;
}

function show_detail_window() {
    document.getElementById("info_box").style.opacity = "0.2";
    document.getElementById("detail_box").style.display = "block";
}

function close_detail_window() {
    document.getElementById("info_box").style.opacity = "1";
    document.getElementById("detail_box").style.display = "none";
}

function show_deploy_task() {
    document.getElementById("home_box").style.opacity = "0.2";
    document.getElementById("deploy_task").style.display = "block";
    document.getElementById("deploy_task").style.opacity = "1";
}

function close_deploy_task() {
    document.getElementById("home_box").style.opacity = "1";
    document.getElementById("deploy_task").style.display = "none";
}

function close_create_task() {
    document.getElementById("deploy_task").style.opacity = "1";
    document.getElementById("create_task").style.display = "none";
}

function clientid_issame(){
    var index=false;
    for(var i=0;i<client_num-1;i++){
        for(var j=i+1;j<client_num;j++){
            if(document.getElementsByName('client_id')[i].value === document.getElementsByName('client_id')[j].value)
                index=true;
        }
    }
    return index;
}

function complete_create_task() {
    if(clientid_issame()) {
        swal("请确保不同client的id不同!","","error");
    }
    else {
        document.getElementById("deploy_task").style.opacity = "1";
        document.getElementById("create_task").style.display = "none";
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent("data:"));
        element.href += "\n  x_train:";
        element.href += "\n" + document.getElementById('x_train').value;
        element.href += "\n  y_train:";
        element.href += "\n" + document.getElementById('y_train').value;
        element.href += "\n  x_test:";
        element.href += "\n" + document.getElementById('x_test').value;
        element.href += "\n  y_test:";
        element.href += "\n" + document.getElementById('y_test').value;
        element.href += "\n  part_num: " + document.getElementById('client_num').value;
        element.href += "\n  client_id: " + document.getElementById('client_id').value;
        element.href += "\n  split_data: " + document.getElementById('split_data').value;
        element.href += "\n\nmodel:";
        element.href += "\n  filepath: " + document.getElementById('filepath').value;
        element.href += "\n  module: " + document.getElementById('module').value;
        element.href += "\n  function: " + document.getElementById('function').value;
        element.href += "\n  optimizer: " + document.getElementById('optimizer').value;
        element.href += "\n  learning_rate: " + document.getElementById('learning_rate').value;
        element.href += "\n  loss: " + document.getElementById('loss').value;
        element.href += "\n  model_type: " + document.getElementById('model_type').value;
        element.href += "\n\ndevice:";
        //var n = document.getElementsByName('client_id').length; //client_num
        element.href += "\n  device1:";
        element.href += "\n    type: " + document.getElementsByName('type')[0].value;
        element.href += "\n    server_id: " + document.getElementById('server_id').value;
        element.href += "\n    execution_form: " + document.getElementById('execution_form').value;
        element.href += "\n    aggregation_type: " + document.getElementById('aggregation_type').value;
        element.href += "\n    aggregation_func: " + document.getElementById('aggregation_func').value;
        element.href += "\n    maxround: " + document.getElementById('maxround').value;
        element.href += "\n    sim_cc: " + document.getElementById('sim_cc').value;
        element.href += "\n    sim_zip_path: " + document.getElementById('sim_zip_path').value;
        element.href += "\n    target_acc: " + document.getElementById('target_acc').value;
        for (i = 0; i < client_num; i++) {
            var j = i + 2;
            element.href += "\n\n  device" + String(j) + ":";
            element.href += "\n    type: " + document.getElementsByName('type')[i + 1].value;
            element.href += "\n    client_id: " + document.getElementsByName('client_id')[i].value;
            element.href += "\n    w_file_initial: " + document.getElementsByName('w_file_initial')[i].value;
            element.href += "\n    batch_size: " + document.getElementsByName('batch_size')[i].value;
            element.href += "\n    train_epoch: " + document.getElementsByName('train_epoch')[i].value;
        }
        var filename = "test.yaml";
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        swal({
            title: "请选择配置文件保存路径!",
            text: "",
            type: "info",
            confirmButtonText: "OK",
        }, function(isConfirm) {
            if (isConfirm) {
                element.click();
                sleep(3000).then(() => {
                    swal("完成配置!", "请上传您的配置文件", "success");
                });
            }
        });
        document.body.removeChild(element);
        /*
        if(document.getElementsByTagName("a"))
            swal("find!");
        else
            swal("not find!");*/
    }
}

function complete_set() {
    var servicename = document.getElementById('servicename1').value;
    var Token = document.getElementById('token').innerHTML;
    window.maxround = document.getElementById('maxround').value;
    window.aggregationtiming = document.getElementById('aggregationtiming').value;
    window.epsilon = document.getElementById('epsilon').value;
    window.batchsize = document.getElementById('batchsize').value;
    window.lr = document.getElementById('lr').value;
    var r = /^[+-]?([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?$/;
    var r_1 = /^[1-9]$|^[1-9][0-9]$/;
    if(r.test(maxround)&&r_1.test(maxround)&&r.test(epsilon)&&r.test(batchsize)&&r_1.test(batchsize)&&r.test(lr)) { // 验证格式是否正确
        document.getElementById('maxround').value = window.maxround;
        document.getElementById('aggregationtiming').value = window.aggregationtiming;
        document.getElementById('epsilon').value = window.epsilon;
        document.getElementById('batchsize').value = window.batchsize;
        document.getElementById('lr').value = window.lr;
        var strategies = {
            "maxround": maxround,
            "aggregationtiming": aggregationtiming,
            "epsilon": epsilon,
            "batchsize": batchsize,
            "lr": lr
        };
        var xmlhttp;
        if (window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
        } else {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        // 发送POST-JSON请求
        xmlhttp.open("POST", "/api/strategy_set/", true);  //login接口
        xmlhttp.setRequestHeader("Content-type", "application/json");
        xmlhttp.send(JSON.stringify({"token": Token, "servicename": servicename, "strategies": strategies}));
        var source = new EventSource('/api/sse_message?channel=event');
        source.onmessage = function (e) {
            if (e.data != 1) {
                var code = e.data.slice(8, 11);
                if (code == "202") {
                    document.getElementById("tasklist_box").style.opacity = "1";
                    document.getElementById("strategy").style.display = "none";
                    document.getElementById("setting").innerHTML = "训练中";
                    document.getElementById("setting").style.opacity = "0.5";
                } else if (code == "201") {
                    document.getElementById("setting").innerHTML = "训练完成";
                    setTimeout(function () {
                        document.getElementById("setting").style.opacity = "1";
                        document.getElementById("setting").innerHTML = "设置策略";
                    }, 2000);
                }
            }
        };
    }
    else{
        swal("请确认各参数格式是否正确!","","warning");
    }
}

function test2() {
    alertTips();
    document.getElementById('servicename2').value="Service2";
    document.getElementById('servicebrief2').value="trainable";
    document.getElementById('servicedetail2').value="Service2 able to be trained";
}

$(function() {
    //当点击"上传配置文件"按钮的时候,触发表单中的浏览文件的操作
    $("#upload_file").click(function() {
        swal({
            title: "请选择已创建的配置文件!",
            text: "",
            type: "info",
            showCancelButton: true,
            confirmButtonText: "OK",
        }, function(isConfirm) {
            if (isConfirm) {
                $("#choose_file").click();
            }
        });
    })
    //当选择好上传文件后,执行提交表单的操作
    $("#choose_file").change(function() {
        var filename=$("#choose_file").val();
        var flag1= filename.endsWith(".yaml");
        if(flag1){//判断是否是所需要的文件类型,这里使用的是yaml文件
            swal("上传文件成功!","","success");
            //$('#submit_file').click();
        }else{
            swal("请选择正确的配置文件!","","error");
        }
    })
    $("#create_file").click(function() {
        document.getElementById("create_task").style.display = "block";
        document.getElementById("deploy_task").style.opacity = "0";
    })
});

function OnInput (event) {
    var n=event.target.value;
    for (var i = 0; i < max_num; i++) {  //动态显示更多client
        document.getElementsByName('client_group')[i].style.display = "none";
        document.getElementsByName('type_group')[i].style.display = "none";
        document.getElementsByName('client_id_group')[i].style.display = "none";
        document.getElementsByName('w_file_initial_group')[i].style.display = "none";
        document.getElementsByName('batch_size_group')[i].style.display = "none";
        document.getElementsByName('train_epoch_group')[i].style.display = "none";
    }
    client_num = n;
    for (var i = 0; i < n; i++) {  //动态显示更多client
        document.getElementsByName('client_group')[i].style.display = "block";
        document.getElementsByName('type_group')[i].style.display = "block";
        document.getElementsByName('client_id_group')[i].style.display = "block";
        document.getElementsByName('w_file_initial_group')[i].style.display = "block";
        document.getElementsByName('batch_size_group')[i].style.display = "block";
        document.getElementsByName('train_epoch_group')[i].style.display = "block";
        document.getElementsByName('client_id')[i].value = "client" + String(i + 1);
        var label = document.getElementsByName('device_client')[i];
        label.innerHTML = "device_client_" + String(i + 1);
    }
    /* append更多client
    for(var i=1;i<=client_num-k;i++) {
        $("#create_task_form").append("<div class=\"form-group\">\n" +
            "            <label for=\"password\" class=\"device_client\" id=\"device_client\" name=\"device_client\" style=\"font-size: 17px;color: darkred;margin-left: 15px\">device_client:</label>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\">\n" +
            "            <label for=\"password\" class=\"col-sm-2 control-label\" style=\"margin-left: -11px\">type</label>\n" +
            "            <div class=\"col-sm-10\" style=\"margin-left: 12px\">\n" +
            "                <select class=\"group\" id=\"type\" name=\"type\">\n" +
            "                    <option value=\"server\">server</option>\n" +
            "                    <option value=\"client\" selected>client</option>\n" +
            "                </select>\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\">\n" +
            "            <label for=\"password\" class=\"col-sm-2 control-label\" >client_id</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"client_id\" name=\"client_id\" value=\"client2\">\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\">\n" +
            "            <label for=\"password\" class=\"col-sm-2 control-label\" >w_file_initial</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"w_file_initial\" name=\"w_file_initial\" value=\"../../../model/MNIST/w0.h5\">\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\">\n" +
            "            <label for=\"password\" class=\"col-sm-2 control-label\" >batch_size</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"batch_size\" name=\"batch_size\" value=\"128\">\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\">\n" +
            "            <label for=\"password\" class=\"col-sm-2 control-label\" >train_epoch</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"train_epoch\" name=\"train_epoch\" value=\"5\">\n" +
            "            </div>\n" +
            "        </div>");
        //var j = document.getElementsByName('device_client').length;
        //document.getElementsByName('device_client')[j-1].value += String(i);
    }*/
}

function validator(){
    $('form').bootstrapValidator({
        fields: {
            celue1: {
                validators: {
                    notEmpty: {
                        message: '策略不能为空'
                    },
                    digits: { //只能是数字
        				message: "该参数只能为整数！"
        			},
                    regexp: { //使用正则
                        regexp: /^[1-9]$|^[1-9][0-9]$/, //验证是不是字母和空格
                        message: '该参数的范围只能在1-99之间!'
                    }
                }
            },
            celue2: {
                validators: {
                    notEmpty: {
                        message: '策略不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /^[A-Z\s]+$/i, //验证是不是字母和空格
                        message: '该参数只能由字母和空格组成!'
                    }
                }
            },
            celue3: {
                validators: {
                    notEmpty: {
                        message: '策略不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /^[+-]?([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?$/, //验证是不是数字
                        message: '该参数只能为整数或者小数!'
                    }
                }
            },
            celue4: {
                validators: {
                    notEmpty: {
                        message: '策略不能为空'
                    },
                    digits: { //只能是数字
        				message: "该参数只能为整数！"
        			},
                    regexp: { //使用正则
                        regexp: /^[1-9]$|^[1-9][0-9]$/, //验证是不是字母和空格
                        message: '该参数的范围只能在1-99之间!'
                    }
                }
            },
            celue5: {
                validators: {
                    notEmpty: {
                        message: '策略不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /^[+-]?([0-9]*\.?[0-9]+|[0-9]+\.?[0-9]*)([eE][+-]?[0-9]+)?$/, //验证是不是数字
                        message: '该参数只能为整数或者小数!'
                    }
                }
            },
            client_num: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[1-9]\d*$)/, //验证是不是数字
                        message: '用户数只能为正整数!'
                    }
                }
            },
            learning_rate: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /^(|\+)?\d+(\.\d+)?$/, //验证是不是正数
                        message: '学习率只能为正数!'
                    }
                }
            },
            maxround: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[1-9]\d*$)/, //验证是不是数字
                        message: '最大轮数只能为正整数!'
                    }
                }
            },
            target_acc: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /^0\.\d+$/, //验证是不是正数 /^(([^0][0-9]+|0)\.([0-9]{1,9}))$/
                        message: '目标准确率只能为小于1大于0的小数!'
                    }
                }
            },
            batch_size: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[1-9]\d*$)/, //验证是不是数字
                        message: '批大小只能为正整数!'
                    }
                }
            },
            train_epoch: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[1-9]\d*$)/, //验证是不是数字
                        message: '训练轮次只能为正整数!'
                    }
                }
            },
            function: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /^[A-Za-z0-9\_]+$/,
                        message: '函数名不能包含特殊符号!'
                    }
                }
            },
            x_train: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[A-Za-z]{1}:\/|^\/)([\w]*\/)*\w+\.{1}[a-zA-Z0-9]+$/,
                        message: '请输入正确的绝对文件地址!'
                    }
                }
            },
            x_test: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[A-Za-z]{1}:\/|^\/)([\w]*\/)*\w+\.{1}[a-zA-Z0-9]+$/,
                        message: '请输入正确的绝对文件地址!'
                    }
                }
            },
            y_train: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[A-Za-z]{1}:\/|^\/)([\w]*\/)*\w+\.{1}[a-zA-Z0-9]+$/, // /^[A-Za-z0-9\_\.\/\[\'\]]+$/,
                        message: '文件地址不能包含特殊符号!'
                    }
                }
            },
            y_test: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[A-Za-z]{1}:\/|^\/)([\w]*\/)*\w+\.{1}[a-zA-Z0-9]+$/, // /^[A-Za-z0-9\_\.\/\[\'\]]+$/,
                        message: '文件地址不能包含特殊符号!'
                    }
                }
            },
            filepath: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[A-Za-z]{1}:\/|^\/)([\w]*\/)+$/, //验证是不是文件地址 /^[A-Za-z0-9\_\.\/\-\+\=\'\~\&\^\$\#\@\!\(\)\[\]\%]+$/
                        message: '请输入正确的绝对文件地址!'
                    }
                }
            },
            sim_zip_path: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[A-Za-z]{1}:\/|^\/)([\w]*\/)+$/, //验证是不是文件地址
                        message: '请输入正确的绝对文件地址!'
                    }
                }
            },
            w_file_initial: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
                    },
                    regexp: { //使用正则
                        regexp: /(^[A-Za-z]{1}:\/|^\/)([\w]*\/)*\w+\.{1}[a-zA-Z0-9]+$/, //验证是不是文件地址
                        message: '模型文件地址应为正确的绝对地址!'
                    }
                }
            },
        }
    });
}

$(function () {
    $("#client_num").change(function() {
       //alert("事件监听");
       validator();
    });
    for(var i=0;i<max_num;i++){
       $("#create_task_form").append("<div class=\"form-group\" id=\"client_group\" name=\"client_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"device_client\" id=\"device_client\" name=\"device_client\" style=\"font-size: 17px;color: darkred;margin-left: 15px\">device_client:</label>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\" id=\"type_group\" name=\"type_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"col-sm-2 control-label\" style=\"margin-left: -11px\">type</label>\n" +
            "            <div class=\"col-sm-10\" style=\"margin-left: 12px\">\n" +
            "                <select class=\"group\" id=\"type\" name=\"type\">\n" +
            "                    <option value=\"server\">server</option>\n" +
            "                    <option value=\"client\" selected>client</option>\n" +
            "                </select>\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\" id=\"client_id_group\" name=\"client_id_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"col-sm-2 control-label\" >client_id</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"client_id\" name=\"client_id\" value=\"client2\">\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\" id=\"w_file_initial_group\" name=\"w_file_initial_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"col-sm-2 control-label\" >w_file_initial</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"w_file_initial\" name=\"w_file_initial\" value=\"D:/model/MNIST/w0.h5\">\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\" id=\"batch_size_group\" name=\"batch_size_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"col-sm-2 control-label\" >batch_size</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"batch_size\" name=\"batch_size\" value=\"128\">\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\" id=\"train_epoch_group\" name=\"train_epoch_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"col-sm-2 control-label\" >train_epoch</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"train_epoch\" name=\"train_epoch\" value=\"5\">\n" +
            "            </div>\n" +
            "        </div>");
    }
    validator();
});



