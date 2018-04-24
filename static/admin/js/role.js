$(function () {
    change_($('select[name="role_type"]'));
    $('select[name="role_type"]').change(function(){
        change_($(this));
    })

    function change_(obj)
    {
        var val = obj.val();
        if(val == 1)
           $('#pri_').hide()
        else
           $('#pri_').show()
    }
    $(".del_role").on('click',function (event) {
        event.preventDefault();
        var role_id   = $(this).attr('data-id').trim();
        var trE = $(this).parent().parent();
        zlalert.alertConfirm({"title":'删除角色',"msg":'确认删除当前角色吗？','cancelCallback':function () {
                return
            },"confirmCallback":function(){
                myajax.get({
                url: "/admin/roledel/",
                data: {"id":role_id},
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
