$(function () {
    $(".del_user").on('click',function (event) {
        event.preventDefault();
        var user_id   = $(this).attr('data-id').trim();
        var trE = $(this).parent().parent();
        zlalert.alertConfirm({"title":'删除用户',"msg":'确认删除当前用户吗？','cancelCallback':function () {
                return
            },"confirmCallback":function(){
                myajax.get({
                url: "/admin/userdel/",
                data: {"id":user_id},
                type:'get',
                dataType: "json",
                success:function(result){
                    if (result.code == 200) {
                        zlalert.alertSuccessToast(result.message);
                        trE.remove()
                    } else {
                        zlalert.alertInfo(result.message);
                    }
                },
                error:function (error) {
                    zlalert.alertError('未连接上服务器')
                }
            })
        }})


    })

})