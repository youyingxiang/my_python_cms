$(function () {
    $("#send_captche").on('click',function (event) {
        event.preventDefault();
        var email   = $("input[name='email']").val().trim();
        if (!email) {
            zlalert.alertInfo('请输入正确邮箱地址')
        }
        myajax.get({
            url: "/admin/email_captche/",
            data: {"email":email},
            type:'get',
            dataType: "json",
            success:function(result){
                if (result.code == 200) {
                    zlalert.alertSuccessToast(result.message);
                } else {
                    zlalert.alertInfo(result.message);
                }
            },
            error:function (error) {
                zlalert.alertNetworkError('未连接上服务器')
            }
        })
    })

    $("#submit").on('click',function(event){
        event.preventDefault();
        var emailE   = $("input[name='email']");
        var captcheE = $("input[name='captche']");
        var email    = emailE.val().trim();
        var captche  = captcheE.val().trim();
        if (!email)
            return '邮箱不能为空！';
        if (!captche)
            return '验证码不能为空！';
        myajax.post({
            url: "/admin/resetemail/",
            data: {"email":email,'captche':captche},
            type:'post',
            dataType: "json",
            success:function(result){
                if (result.code == 200) {
                    zlalert.alertSuccessToast(result.message);
                    emailE.val('');
                    captcheE.val('');
                } else {
                    zlalert.alertInfo(result.message);
                }
            },
            error:function (error) {
                zlalert.alertNetworkError('未连接上服务器')
            }
        })

    })

})