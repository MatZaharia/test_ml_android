var maxround;
var epsilon;
var aggregationtiming;
var batchsize;
var lr;
var token;
var client_num=1;
var max_num=100;
var add_height = 130;
var ori_left = 0;
var ori_top = 0;
var id_num = [0,0,0,0,0];
var main_num = [0,0]

window.onload = function(){
    var xmlhttp;
    xmlhttp = new XMLHttpRequest();
    var Token = document.getElementById('token').innerHTML;
    xmlhttp.open("POST", "/api/uploadfile_info/", true);
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send(JSON.stringify({"token": Token}));
    xmlhttp.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {//验证请求是否发送成功
            var json = xmlhttp.responseText;  //获取到服务端返回的数
            json = JSON.parse(json);
            if (json['code'] == 200) {
                var uploadfile_info = json['data'];
                var uploadfile_len = uploadfile_info.length;
                for(var i=0; i<uploadfile_len;i++){
                    document.getElementById('uploadedfile_name'.concat(i+1)).innerHTML=uploadfile_info[i][0];
                    document.getElementById('uploadedtime'.concat(i+1)).innerHTML=uploadfile_info[i][1];
                }
            } else if(json['code'] == 400) {
                swal("获取上传文件参数失败!","","error",function (isConfirm){if(isConfirm){window.location.href = "/login/";}});
            }
        }
    }

    var xmlhttp1;
    xmlhttp1 = new XMLHttpRequest();
    xmlhttp1.open("POST", "/api/createfile_info/", true);
    xmlhttp1.setRequestHeader("Content-type", "application/json");
    xmlhttp1.send(JSON.stringify({"token": Token}));
    xmlhttp1.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (xmlhttp1.readyState == 4 && xmlhttp1.status == 200) {//验证请求是否发送成功
            var json = xmlhttp1.responseText;  //获取到服务端返回的数
            json = JSON.parse(json);
            if (json['code'] == 200) {
                var createfile_info = json['data'];
                var createfile_len = createfile_info.length;
                for(var i=0; i<createfile_len;i++){
                    document.getElementById('createdfile_name'.concat(i+1)).innerHTML = createfile_info[i][0];
                    document.getElementById('createdtime'.concat(i+1)).innerHTML = createfile_info[i][1];
                }
            } else if(json['code'] == 400) {
                swal("获取上传文件参数失败!","","error",function (isConfirm){if(isConfirm){window.location.href = "/login/";}});
            }
        }
    }
}

function salert(){
    swal("成功跳转!", "", "success");
    alert(getTime());
}

function addzero(num){
    if(num < 10)
        return '0'+String(num)
    else
        return String(num)
}

function sleep(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

function getTime(){
    var now = new Date();
    var year = now.getFullYear(); //得到年份
    var month = now.getMonth()+1;//得到月份
    var date = now.getDate();//得到日期
    var hour= now.getHours();//得到小时数
    var minute= now.getMinutes();//得到分钟数
    var second= now.getSeconds();//得到秒数
    var myDate = String(year)+'.'+String(month)+'.'+String(date)+'-'+addzero(hour)+':'+addzero(minute)+':'+addzero(second)
    return myDate
}

function getTime1(){
    var now = new Date();
    var year = now.getFullYear(); //得到年份
    var month = now.getMonth()+1;//得到月份
    var date = now.getDate();//得到日期
    var hour= now.getHours();//得到小时数
    var minute= now.getMinutes();//得到分钟数
    var second= now.getSeconds();//得到秒数
    var myDate = String(month)+'_'+String(date)+'_'+addzero(hour)+'_'+addzero(minute)+'_'+addzero(second)
    return myDate
}

function show_home(){
    if(document.getElementById("task_deploy").style.display === "none"){
        document.getElementById("task_deploy").style.display = "block";
        document.getElementById("uploaded_model").style.display = "block";
        document.getElementById("client_reward").style.display = "block";
        var Height = $('#option').height();
        $("#option").css({height: Height+add_height+10+'px'});
    }
    else {
        document.getElementById("task_deploy").style.display = "none";
        document.getElementById("uploaded_model").style.display = "none";
        document.getElementById("client_reward").style.display = "none";
        var Height = $('#option').height();
        $("#option").css({height: Height-add_height+'px'});
    }
}
function show_infolist(){
    if(document.getElementById("global_model").style.display === "none"){
        document.getElementById("global_model").style.display = "block";
        document.getElementById("weight").style.display = "block";
        document.getElementById("train_client").style.display = "block"
        var Height = $('#option').height();
        $("#option").css({height: Height+add_height+10+'px'});
    }
    else {
        document.getElementById("global_model").style.display = "none";
        document.getElementById("weight").style.display = "none";
        document.getElementById("train_client").style.display = "none";
        var Height = $('#option').height();
        $("#option").css({height: Height-add_height+'px'});
    }
}

function show_task_deploy(){
    window.location.href = "/homepage_2/";
}

function show_global_model(){
    window.location.href = "/homepage_3/";
}

function show_userpage(){
    window.location.href = "/homepage_5/";
}

function cancel_create_task(){
    window.location.href = "/homepage_2/";
}

function show_tasklist(){
    window.location.href = "/homepage_4/";
}

function show_clientinfo(){
    window.location.href = "/homepage_clientinfo/";
}

function isInteger(obj) {
 return Math.floor(obj) === obj
}

function OnInput (event) {
    var n=event.target.value;
    n=parseInt(n);
    if(!isInteger(n))
        return;
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
    if (clientid_issame()) {
        swal("请确保不同client的id不同!", "", "error");
    } else {
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
        element.href += "\n  device1:";
        element.href += "\n    type: " + document.getElementsByName('type')[0].value;
        element.href += "\n    server_id: " + document.getElementById('server_id').value;
        // var server_id = document.getElementById('server_id').value;
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
        var now_time = getTime();
        var filename = "Config_"+getTime1()+".yaml";
        element.setAttribute('download', filename);
        // 后续跟后端同学沟通一下，设置参数后应该不用保存成.yaml再上传，可以直接上传json数据给后端接口读取
        element.style.display = 'none';
        swal({
            title: "已创建配置文件!",
            text: "请选择上传或下载配置文件",
            type: "success",
            showCancelButton: true,
            cancelButtonColor: "#DD6B55",
            confirmButtonText: "下载",
            cancelButtonText: "上传",
        }, function (isConfirm) {
            if (isConfirm) {
                element.click();
                // 给后端接口发送文件流

                //
                var xmlhttp;
                // 记录历史创建数据
                xmlhttp = new XMLHttpRequest();
                var Token = document.getElementById('token').innerHTML;
                xmlhttp.open("POST", "/api/create_file/", true);  //home主页接口
                xmlhttp.setRequestHeader("Content-type", "application/json");
                xmlhttp.send(JSON.stringify({"token": Token, "file_info": {"filename": filename, "time": now_time}}));
                xmlhttp.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
                    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {//验证请求是否发送成功
                        var json = xmlhttp.responseText;  //获取到服务端返回的数
                        json = JSON.parse(json);
                        if (json['code'] == 200) {
                            sleep(3000).then(() => {
                                swal({
                                    title: "已下载配置文件!",
                                    type: "success",
                                    confirmButtonText: "OK"
                                }, function (isConfirm){
                                    if(isConfirm){
                                        window.location.href = "/homepage_2/";
                                    }
                                });
                            });
                        } else if(json['code'] == 400) {
                            swal("记录创建参数失败!","","error",function (isConfirm){if(isConfirm){window.location.href = "/login/";}});
                        }
                    }
                }
            }
            else{
                var xmlhttp;
                xmlhttp = new XMLHttpRequest();
                var Token = document.getElementById('token').innerHTML;
                xmlhttp.open("POST", "/api/upload_file/", true);  //home主页接口
                xmlhttp.setRequestHeader("Content-type", "application/json");
                xmlhttp.send(JSON.stringify({"token": Token, "file_info": {"filename": filename, "time": now_time}}));
                xmlhttp.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
                    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {//验证请求是否发送成功
                        var json = xmlhttp.responseText;  //获取到服务端返回的数
                        json = JSON.parse(json);
                        if (json['code'] == 200) {
                            swal({
                                title: "已上传配置文件!",
                                type: "success",
                                confirmButtonText: "OK"
                            }, function (isConfirm){
                                if(isConfirm){
                                    window.location.href = "/homepage_2/";
                                }
                            });
                        } else if(json['code'] == 400) {
                            window.location.href = "/login/"; //跳转任务列表界面连接
                        }
                    }
                }
            }
        });
        document.body.removeChild(element);
    }
}

function show_seting(event){
    var id = event.target.id;
    var n = id[15];
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
    xmlhttp.send(JSON.stringify({"token": Token, "id": n}));
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
                // 只实现一个请求的信息填充
                document.getElementById('servicename'.concat(n)).innerHTML=servicename;
                document.getElementById('servicebrief'.concat(n)).innerHTML=servicebrief;
                document.getElementById('servicedetail'.concat(n)).innerHTML=servicedetail;
                document.getElementsByName('maxround')[n-1].value = window.maxround;
                document.getElementsByName('aggregationtiming')[n-1].value = window.aggregationtiming;
                document.getElementsByName('epsilon')[n-1].value = window.epsilon;
                document.getElementsByName('batchsize')[n-1].value = window.batchsize;
                document.getElementsByName('learning_rate')[n-1].value = window.lr;
            } else if(json['code'] == 400) {
                swal("请求设置失败!","","error");
                window.location.href = "/login/"; //跳转任务列表界面连接
            }
        }
    }
    var k = document.getElementsByName('request').length;
    for (var i = 0; i < k; i++) {
        document.getElementsByName('request')[i].style.display = "none";
    }
    document.getElementById("seting_strategy".concat(n)).style.display = "none";
    document.getElementById("set_strategy_box".concat(n)).style.display = "block";
    var o_left = (document.getElementsByName('request')[n-1].style.left).replace('px','');
    window.ori_left = parseInt(o_left);
    var o_top = (document.getElementsByName('request')[n-1].style.top).replace('px','');
    window.ori_top = parseInt(o_top);
    document.getElementsByName('request')[n-1].style.left = 270+'px';
    document.getElementsByName('request')[n-1].style.top = 170+'px';
    document.getElementsByName('request')[n-1].style.display = "block";
}

function cancel_set(event){
    var id = event.target.id;
    var n = id[10];
    document.getElementsByName('request')[n-1].style.left = window.ori_left+'px';
    document.getElementsByName('request')[n-1].style.top = window.ori_top+'px';
    var k = document.getElementsByName('request').length;
    for (var i = 0; i < k; i++) {  //动态显示更多client
        document.getElementsByName('request')[i].style.display = "block";
    }
    document.getElementById("set_strategy_box".concat(n)).style.display = "none";
    document.getElementById("seting_strategy".concat(n)).style.display = "block";
}

function complete_set(event) {
    var id = event.target.id;
    var n = id[12];
    var servicename = document.getElementById("servicename".concat(n)).innerHTML;
    var Token = document.getElementById('token').innerHTML;
    window.maxround = document.getElementsByName('maxround')[n-1].value;
    window.aggregationtiming = document.getElementsByName('aggregationtiming')[n-1].value;
    window.epsilon = document.getElementsByName('epsilon')[n-1].value;
    window.batchsize = document.getElementsByName('batchsize')[n-1].value;
    window.lr = document.getElementsByName('learning_rate')[n-1].value;
    var r1 = /(^[1-9]\d*$)/;
    var r2 = /^(|\+)?\d+(\.\d+)?$/
    if(r1.test(maxround)&&r2.test(epsilon)&&r1.test(batchsize)&&r2.test(lr)) { // 验证格式是否正确
        document.getElementsByName('maxround')[n-1].value = window.maxround;
        document.getElementsByName('aggregationtiming')[n-1].value = window.aggregationtiming;
        document.getElementsByName('epsilon')[n-1].value = window.epsilon;
        document.getElementsByName('batchsize')[n-1].value = window.batchsize;
        document.getElementsByName('learning_rate')[n-1].value = window.lr;
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
                swal({
                        title: "设置成功!",
                        text: "",
                        type: "success"
                    },function (isConfirem){
                        if(isConfirem){
                            document.getElementById("seting_strategy".concat(n)).innerHTML = "训练中";
                            document.getElementById("seting_strategy".concat(n)).style.opacity = "0.5";
                            document.getElementsByName('request')[n - 1].style.left = window.ori_left + 'px';
                            document.getElementsByName('request')[n - 1].style.top = window.ori_top + 'px';
                            var k = document.getElementsByName('request').length;
                            for (var i = 0; i < k; i++) {  //动态显示更多client
                                document.getElementsByName('request')[i].style.display = "block";
                            }
                            document.getElementById("set_strategy_box".concat(n)).style.display = "none";
                            document.getElementById("seting_strategy".concat(n)).style.display = "block";
                        }
                    });
                }
            }
        };
        // source.onmessage = function (e) {
        //     if (e.data != 1) {
        //         var code = e.data.slice(8, 11);
        //         if (code == "202") {
        //             swal("设置成功!","","success");
        //             document.getElementById("complete_set".concat(n)).innerHTML = "训练中";
        //             document.getElementById("complete_set".concat(n)).style.opacity = "0.5";
        //         } else if (code == "201") {
        //             document.getElementById("complete_set".concat(n)).innerHTML = "训练完成";
        //             setTimeout(function () {
        //                 document.getElementById("complete_set".concat(n)).style.opacity = "1";
        //                 document.getElementById("complete_set".concat(n)).innerHTML = "完成设置";
        //             }, 2000);
        //             swal({
        //                     title: "训练完成!",
        //                     text: "",
        //                     type: "success"
        //                 }, function (isConfirm) {
        //                     if (isConfirm) {
        //                         document.getElementsByName('request')[n-1].style.left = window.ori_left+'px';
        //                         document.getElementsByName('request')[n-1].style.top = window.ori_top+'px';
        //                         var k = document.getElementsByName('request').length;
        //                         for (var i = 0; i < k; i++) {  //动态显示更多client
        //                             document.getElementsByName('request')[i].style.display = "block";
        //                         }
        //                         document.getElementById("set_strategy_box".concat(n)).style.display = "none";
        //                         document.getElementById("seting_strategy".concat(n)).style.display = "block";
        //                     }
        //             });
        //         }
        //     }
        // };
    }
    else{
        swal("请确认各参数格式是否正确!","","warning");
    }
}

function modify_userinfo(){
    document.getElementById("complete_modify_userinfo").style.display = "inline-block";
    document.getElementById("modify_userinfo").style.display = "none";
    $("#task_num").removeAttr("disabled","disabled");
    $("#cluster_num").removeAttr("disabled","disabled");
    $("#active_state").removeAttr("disabled","disabled");
    $("#manage_time").removeAttr("disabled","disabled");
    $("#related_info").removeAttr("disabled","disabled");
    $("#max_tasknum").removeAttr("disabled","disabled");
    $("#max_clusternum").removeAttr("disabled","disabled");
    $("#consume_resource").removeAttr("disabled","disabled");
    $("#survive_time").removeAttr("disabled","disabled");
    $("#other").removeAttr("disabled","disabled");
}

function complete_modify_userinfo(){
    document.getElementById("complete_modify_userinfo").style.display = "none";
    document.getElementById("modify_userinfo").style.display = "inline-block";
    $("#task_num").attr("disabled","disabled");
    $("#cluster_num").attr("disabled","disabled");
    $("#active_state").attr("disabled","disabled");
    $("#manage_time").attr("disabled","disabled");
    $("#related_info").attr("disabled","disabled");
    $("#max_tasknum").attr("disabled","disabled");
    $("#max_clusternum").attr("disabled","disabled");
    $("#consume_resource").attr("disabled","disabled");
    $("#survive_time").attr("disabled","disabled");
    $("#other").attr("disabled","disabled");
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
        var filename=$("#choose_file").val().substring(12);
        var now_time = getTime();
        var flag1= filename.endsWith(".yaml");
        if(flag1){//判断是否是所需要的文件类型,这里使用的是yaml文件
            swal({
                title: "上传文件成功!",
                text: "",
                type: "success"
            },function (isConfirm){
                if(isConfirm){
                    // 记录上传文件信息
                    var xmlhttp;
                    xmlhttp = new XMLHttpRequest();
                    var Token = document.getElementById('token').innerHTML;
                    xmlhttp.open("POST", "/api/upload_file/", true);  //home主页接口
                    xmlhttp.setRequestHeader("Content-type", "application/json");
                    xmlhttp.send(JSON.stringify({"token": Token, "file_info": {"filename": filename, "time": now_time}}));
                    xmlhttp.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
                        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {//验证请求是否发送成功
                            var json = xmlhttp.responseText;  //获取到服务端返回的数
                            json = JSON.parse(json);
                            if (json['code'] == 200) {

                            } else if(json['code'] == 400) {
                                window.location.href = "/login/"; //跳转任务列表界面连接
                            }
                        }
                    }
                }
            });
        }else{
            swal("请选择正确的配置文件!","","error");
        }
    })
    $("#create_file").click(function() {
        window.location.href = "/homepage_1/";
    })
    $("#logout").click(function() {
        xmlhttp = new XMLHttpRequest();
        var Token = document.getElementById('token').innerHTML;
        xmlhttp.open("POST", "/api/logout/", true);  //home主页接口
        xmlhttp.setRequestHeader("Content-type", "application/json");
        xmlhttp.send(JSON.stringify({"token": Token}));
        xmlhttp.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {//验证请求是否发送成功
                var json = xmlhttp.responseText;  //获取到服务端返回的数
                json = JSON.parse(json);
                if (json['code'] == 200) {
                    window.location.href = "/login/";
                } else if(json['code'] == 400) {

                }
            }
        }
    })
    // $(".remove_client").click(function(event) {
    //     var id = event.target.id;
    //     document.getElementById("Client".concat(id[13])).style.display = "none";
    //     document.getElementById("client_num").innerHTML = document.getElementById("client_num").innerHTML - 1;
    //     var len = document.getElementsByClassName("Client").length;
    //     for(var i = id[13]; i <= 5; i++ ) {
    //         document.getElementById("client_id".concat(i)).innerHTML = "client_"+String(parseInt(document.getElementById("client_id".concat(i)).innerHTML[7]) - 1);
    //     }
    //     var Width = $('#Task1').width();
    //     $("#Task1").css({width: Width-470+'px'});
    // })
    $(".remove_client").click(function(event) {
        var id = event.target.id;
        document.getElementById("client_num0").innerHTML = document.getElementById("client_num0").innerHTML - 1;
        document.getElementById("client_num1").innerHTML = document.getElementById("client_num1").innerHTML - 1;
        document.getElementById("Client".concat(id[13])).style.display = "none";
        document.getElementById("Client_info".concat(id[13])).style.display = "none";
        document.getElementById("client_item".concat(id[13])).style.display = "none";
        for(var i = id[13]; i <= 5; i++ ) {
            $("#client_item".concat(i)).css({left: document.getElementById("client_item".concat(i)).offsetLeft - 540 + 'px'});
            $("#Client".concat(i)).css({left: document.getElementById("client_item".concat(i)).offsetLeft + 'px'});
            $("#Client_info".concat(i)).css({left: document.getElementById("client_item".concat(i)).offsetLeft + 'px'});
        }
    })
    $(".more_client").click(function(event){
        var id = event.target.id;
        var n = id[11];
        document.getElementById("Client_info".concat(n)).style.display = "block";
        }
    )
    $(".modify_clientinfo").click(function(event){
        var id = event.target.id;
        var n = id[17];
        document.getElementById("modify_clientinfo".concat(n)).style.display = "none";
        document.getElementById("complete_modify_clientinfo".concat(n)).style.display = "inline-block";
        $("#learning_rate".concat(n)).removeAttr("disabled","disabled");
        $("#maxround".concat(n)).removeAttr("disabled","disabled");
        $("#active_state".concat(n)).removeAttr("disabled","disabled");
        $("#batchsize".concat(n)).removeAttr("disabled","disabled");
        $("#epsilon".concat(n)).removeAttr("disabled","disabled");
        }
    )
    $(".complete_modify_clientinfo").click(function(event){
        var id = event.target.id;
        var n = id[26];
        document.getElementById("complete_modify_clientinfo".concat(n)).style.display = "none";
        document.getElementById("modify_clientinfo".concat(n)).style.display = "inline-block";
        $("#learning_rate".concat(n)).attr("disabled","disabled");
        $("#maxround".concat(n)).attr("disabled","disabled");
        $("#active_state".concat(n)).attr("disabled","disabled");
        $("#batchsize".concat(n)).attr("disabled","disabled");
        $("#epsilon".concat(n)).attr("disabled","disabled");
        }
    )
    $(".close_clientinfo").click(function(event){
        var id = event.target.id;
        var n = id[16];
        document.getElementById("Client_info".concat(n)).style.display = "none";
        }
    )
    $(".client_item").click(function(event) {
        var id = event.target.id;
        var num = id[11];
        var moreheight = true;
        var lessheight = true;
        $("#Client".concat(num)).toggle("fast",function (){
            if(id_num[parseInt(num)-1] === 1) {
                id_num[parseInt(num)-1] = 0;
                $("#Task1").css({width: $('#Task1').width() - 296 + 'px'});
                for(var i = 0; i<id_num.length;i++) {
                    if(id_num[i] == 1) {
                        lessheight = false;
                        break;
                    }
                }
                if(lessheight) {
                    $("#main1").css({height: $('#main1').height() - 240 + 'px'});
                }
                var len = document.getElementsByClassName("Client").length;
                for(var j=parseInt(num)+1;j<=5;j++){
                    $("#client_item".concat(j)).css({left: document.getElementById("client_item".concat(j)).offsetLeft - 420 + 'px'});
                    $("#Client".concat(j)).css({left: document.getElementById("client_item".concat(j)).offsetLeft + 'px'});
                    $("#Client_info".concat(j)).css({left: document.getElementById("client_item".concat(j)).offsetLeft + 'px'});
                }
            }
            else {
                $("#Client".concat(num)).css({left: document.getElementById("client_item".concat(num)).offsetLeft + 'px'});
                $("#Client_info".concat(num)).css({left: document.getElementById("client_item".concat(num)).offsetLeft + 'px'});
                $("#Task1").css({width: $('#Task1').width() + 300 + 'px'});
                for(var i = 0; i<id_num.length;i++) {
                    if(id_num[i] == 1) {
                        moreheight = false;
                        break;
                    }
                }
                if(moreheight) {
                    $("#main1").css({height: $('#main1').height() + 250 + 'px'});
                }
                var len = document.getElementsByClassName("Client").length;
                for(var i=parseInt(num)+1;i<=5;i++){
                    $("#client_item".concat(i)).css({left: document.getElementById("client_item".concat(i)).offsetLeft + 400 + 'px'});
                    $("#Client".concat(i)).css({left: document.getElementById("client_item".concat(i)).offsetLeft + 'px'});
                    $("#Client_info".concat(i)).css({left: document.getElementById("client_item".concat(i)).offsetLeft + 'px'});
                }
                id_num[parseInt(num)-1] = 1;
            }
        });
    });
    $(".task_item").click(function(event) {
        var id = event.target.id;
        var num = id[9];
        $("#main".concat(num)).toggle("normal",function (){
            if(main_num[parseInt(num)-1] === 1) {  // 从有到无
                if(main_num[0] == 1) {
                    $("#task_item2").css({left: 700 + 'px'});
                    $("#task_item2").css({top: 200 + 'px'});
                    if(main_num[1] == 1)
                        $("#main2").css({top: 250 + 'px'});
                }
                main_num[parseInt(num)-1] = 0;
            }
            else { // 从无到有
                if(main_num[1] == 1) {
                    $("#task_item2").css({left: 300 + 'px'});
                    $("#task_item2").css({top: 600 + 'px'});
                    $("#main2").css({top: 650 + 'px'});
                }
                if(main_num[0] == 1) {
                    $("#task_item2").css({left: 300 + 'px'});
                    $("#task_item2").css({top: 600 + 'px'});
                    $("#main2").css({top: 650 + 'px'});
                }
                main_num[parseInt(num)-1] = 1;
            }
            var dontshow = false;
            for(var i = 0; i < main_num.length; i++) {
                if(main_num[i] == 1){
                    dontshow = true;
                    break;
                }
            }
            var len = document.getElementsByClassName("task_info").length;
            if(dontshow) {
                for (var i = 0; i < len; i++) {
                    document.getElementById("task_info".concat(i+1)).style.display = "none";
                }
            }
            else {
               for (var i = 0; i < len; i++) {
                    document.getElementById("task_info".concat(i+1)).style.display = "block";
                }
            }
        });
    });
});

function validator(){
    $('form').bootstrapValidator({
        fields: {
            epsilon: {
                validators: {
                    notEmpty: {
                        message: '参数不能为空'
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
            epsilon: {
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
                        message: '准确率只能为小于1大于0的小数!'
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
    validator();
    $("#client_num").change(function() {
       //alert("事件监听");
       validator();
    });
    for(var i=0;i<max_num;i++){
       $("#create_client").append("<div class=\"form-group\" id=\"client_group\" name=\"client_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"device_client\" id=\"device_client\" name=\"device_client\" style=\"font-size: 25px;color: darkred; margin-top: 0px; margin-left: 15px\">device_client:</label>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\" id=\"type_group\" name=\"type_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"col-sm-2_control-label\">type</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <select class=\"group\" id=\"type\" name=\"type\" style=\"width: 150px; text-align: center; height: 35px; border-radius: 10px;\">\n" +
            "                    <option value=\"server\">server</option>\n" +
            "                    <option value=\"client\" selected>client</option>\n" +
            "                </select>\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\" id=\"client_id_group\" name=\"client_id_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"col-sm-2_control-label\" >client_id</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"client_id\" name=\"client_id\" value=\"client2\">\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\" id=\"w_file_initial_group\" name=\"w_file_initial_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"col-sm-2_control-label\" >w_file_initial</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"w_file_initial\" name=\"w_file_initial\" value=\"D:/model/MNIST/w0.h5\">\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\" id=\"batch_size_group\" name=\"batch_size_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"col-sm-2_control-label\" >batch_size</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"batch_size\" name=\"batch_size\" value=\"128\">\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        <div class=\"form-group\" id=\"train_epoch_group\" name=\"train_epoch_group\" style=\"display: none\">\n" +
            "            <label for=\"password\" class=\"col-sm-2_control-label\" >train_epoch</label>\n" +
            "            <div class=\"col-sm-10\">\n" +
            "                <input type=\"text\" class=\"form-control\" id=\"train_epoch\" name=\"train_epoch\" value=\"5\">\n" +
            "            </div>\n" +
            "        </div>");
    }
    validator();
});
