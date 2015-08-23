/**
 * Created by wushengyu on 15/8/23.
 */
function submitChangePassword(){
  var origin_password = $('#origin_password').val();
  var new_password = $('#new_password').val();
  var password_again = $('#password_again').val();
  if (origin_password && new_password && password_again){
    if (new_password === password_again){
      $.ajax({
        url: '/user/security_center',
        type: 'post',
        data: {
          origin_password: origin_password,
          new_password: new_password,
          password_again: password_again,
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        dataType: "json",
        success: function(data){
          if (data === 'success'){
            window.location = '/login'
          } else{
            Notify("密码错误");
          }
        }
      });
    } else{
      Notify("新密码两次输入不一致");
    }
  } else{
    Notify("请完善信息");
  }
}