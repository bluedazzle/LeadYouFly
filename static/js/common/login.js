/**
 * Created by wushengyu on 15/8/8.
 */
$(document).ready(function(){
  $("body").keydown(function() {
    if (event.keyCode == "13") {//keyCode=13是回车键
      $('#login_submit').click();
    }
  });

  $('#login_submit').click(function(){
    var account = $('#username').val();
    var password = $('#password').val();
    if (account && password){
      $.ajax({
            url: "/login",
            type: "post",
            data: {
              "username": account,
              "password": password,
              "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "json",
            success: function(data, status){
              if(data === "success"){
                window.location = "/user/complete_mes"
              } else{
                Notify(data);
              }
            }
          }
      )
    }
    else{
      Notify("请填写正确的信息");
    }
  });
});