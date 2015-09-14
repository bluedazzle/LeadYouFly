/**
 * Created by wushengyu on 15/8/8.
 */
$(document).ready(function () {
    var req_url = window.location.pathname + window.location.search;
    $('#user-position').text("我的档案");
    $('#complete_mes_submit').click(function () {
        var qq = $('#qq').val();
        var yy = '';
        var phone = $('#phone').val();
        if (qq && phone && phone.length == 11) {
            $.ajax({
                    url: req_url,
                    type: "post",
                    data: {
                        "qq": qq,
                        "yy": yy,
                        "phone": phone,
                        "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
                    },
                    dataType: "json",
                    success: function (data, status) {
                        if (data.status === "success") {
                            if (data.next_page) {
                                window.location = data.next_page;
                            } else {
                                window.location = "/user/complete_mes";
                            }
                        } else {
                            Notify(data.status);
                        }
                    }
                }
            )
        }
        else {
            Notify("请填写正确的信息");
        }
    });
});