/**
 * Created by Administrator on 2016/12/17.
 */

$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);
        if(that.children('a').attr('href') == '#'){
            event.preventDefault();
        }
        if(that.parent().hasClass('unfold')){
            that.parent().removeClass('unfold');
        }else{
            that.parent().addClass('unfold').siblings().removeClass('unfold');
        }
        console.log('coming....');
    });

    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration','none');
    });
});


$(function () {
    var url = window.document.location.pathname;
    var arr = new Array()
    var arr = url.split('/')
    if (arr.length == 4) {
        action = arr[2]
        $("." + action).parent().parent().addClass('unfold').siblings().removeClass('unfold');
        $("." + action).addClass('active').siblings().removeClass('active');
    }
});