$(function () {
    $("#submit").on('click',function (event) {
        event.preventDefault();
        var oldpwd   = $("input[name='oldpwd']");
        var newpwd   = $("input[name='newpwd']");
        var renewpwd = $("input[name='renewpwd']");
        myajax.post({
            url: "/admin/resetpwd/",
            data: {"oldpwd":oldpwd.val().trim(),'newpwd':newpwd.val().trim(),'renewpwd':renewpwd.val().trim()},
            type:'post',
            dataType: "json",
            success:function(result){
                if (result.code == 200) {
                    zlalert.alertSuccessToast(result.message);
                    oldpwd.val('');
                    newpwd.val('');
                    renewpwd.val('');
                } else {
                    zlalert.alertInfo(result.message);
                }
            },
            error:function (error) {
                zlalert.alertError('未连接上服务器')
            }
        })
    })

})