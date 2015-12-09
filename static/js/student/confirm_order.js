/**
 * Created by RaPoSpectre on 12/7/15.
 */
function createOrder(platform) {
    var qq = '';
    var phone = '';
    var course_id = $('#course').val();
    var csrf_token = $("input[name='csrfmiddlewaretoken']").val();
    var wechatInfo = navigator.userAgent.match(/MicroMessenger\/([\d\.]+)/i);
    var channel = 'alipay';
    if (platform === 'pc') {
        qq = $('#pcQq').val();
        phone = $('#pcPhone').val();
    } else {
        qq = $('#qq').val();
        phone = $('#phone').val();
    }
    if (qq === '' || phone === '') {
        alert('请完善联系信息');
        return false;
    }
    if (wechatInfo) {
        channel = 'wechat';
    }
    var post_dict = {
        'qq': qq,
        'phone': phone,
        'course_id': course_id,
        'channel': channel,
        'csrfmiddlewaretoken': csrf_token
    };
    $.ajax({
        type: 'POST',
        url: '/user/create_order/',
        data: post_dict,
        success: function (data) {
            if (data.status == 1) {
                if (channel == 'alipay') {
                    $('#payModal').modal({backdrop: 'static', keyboard: false});
                    var tempwindow=window.open('_blank');
                    tempwindow.location = data.body.redirect_url;
                } else {
                    //wechat
                }
            }else{
                alert(data.body.err_msg);
            }

        },
        dataType: 'json'
    });
}