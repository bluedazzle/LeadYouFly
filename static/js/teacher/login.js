/**
 * Created by wushengyu on 15/8/8.
 */
$(document).ready(function(){
  $('#login_submit').click(function(){
    var account = $('#username').val();
    var password = $('#password').val();
    if (account && password){
      $.ajax({
            url: "/teacher/login",
            type: "post",
            data: {
              "username": account,
              "password": password,
              "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "json",
            success: function(data, status){
              if(data === "success"){
                window.location = "/teacher/host"
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