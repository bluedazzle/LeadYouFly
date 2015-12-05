/**
 * Created by wushengyu on 15/8/8.
 */
$(document).ready(function () {
    $("body").keydown(function () {
        if (event.keyCode == "13") {//keyCode=13是回车键
            $('#login_submit').click();
        }
    });

    $('#login_submit').click(function () {
        var account = $('#username').val();
        var password = $('#password').val();
        var refer = $('#refer').val();
        if (account && password) {
            $.ajax({
                    url: "/login",
                    type: "post",
                    data: {
                        "username": account,
                        "password": password,
                        "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
                    },
                    dataType: "json",
                    success: function (data, status) {
                        if (data.status === "success") {
                            if (refer != '') {
                                window.location = refer;
                            } else {
                                window.location = "/search_teacher";

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