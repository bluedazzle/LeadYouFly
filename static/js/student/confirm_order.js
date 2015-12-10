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
                    openwin(data.body.data);
                } else {
                    var params = data.body.data;
                    $('#payModal').modal({backdrop: 'static', keyboard: false});
                    WeixinJSBridge.invoke(
                           'getBrandWCPayRequest', params,
                           function(res){
                               if(res.err_msg == "get_brand_wcpay_request：ok" ) {
                                   window.location.href = 'http://lol.fibar.cn/user/my_orders'
                               }     // 使用以上方式判断前端返回,微信团队郑重提示：res.err_msg将在用户支付成功后返回    ok，但并不保证它绝对可靠。
                           }
   );
                }
            }else{
                alert(data.body.err_msg);
            }

        },
        dataType: 'json'
    });
}

function openwin(url) {
    var a = document.createElement("a");
    a.setAttribute("href", url);
    a.setAttribute("target", "_blank");
    a.setAttribute("id", "openwin");
    document.body.appendChild(a);
    a.click();
}