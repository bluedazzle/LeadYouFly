/**
 * Created by wushengyu on 15/9/6.
 */
$(document).ready(function(){
  var count;
  var countdown;
  var verifyButton = $('#get_verify');
  function Count(){
    count--;
    verifyButton.text("请等待"+count+"秒");
    if(count == 0){
      clearInterval(countdown);
      verifyButton.text("获取验证码");
      verifyButton.removeAttr('disabled');
      localStorage.removeItem('verify_time')
    }
  }
  if(localStorage['verify_time']){
    var last_time = parseInt(localStorage['verify_time']);
    var now_time = parseInt(new Date().getTime());
    if(now_time-last_time < 30000){
      count = parseInt(30-(now_time - last_time)/1000);
      verifyButton.text("请等待"+count+"秒");
      verifyButton.attr('disabled', true);
      countdown = setInterval(Count, 1000);
    }
    else{
      localStorage.removeItem('verify_time');
    }
  }
  verifyButton.click(function(){
    var phone_number = $('#phone');
    if(phone_number.val() && phone_number.val().length == 11){
      $.ajax({
        url: "/get_verify_sms_forget?phone=" + phone_number.val(),
        type: "get",
        data: "",
        dataType: "json",
        success: function(data, status){
          if(data == "success"){
            count = 30;
            verifyButton.text("请等待"+count+"秒");
            verifyButton.attr('disabled', true);
            localStorage['verify_time'] = new Date().getTime();
            countdown = setInterval(Count, 1000);
          } else {
            Notify(data);
          }
        }
      })
    } else{
      Notify("请填写正确的手机号")
    }
  });


  $("body").keydown(function() {
    if (event.keyCode == "13") {//keyCode=13是回车键
      $('#submit_form').click();
    }
  });

  $('#submit_form').click(function(){
    var phone = $('#phone').val();
    var verify_code = $('#verify_code').val();
    var password = $('#password').val();
    if (phone && phone.length == 11 && verify_code && password){
      $.ajax({
            url: "/forget_password",
            type: "post",
            data: {
              "phone": phone,
              "verify_code": verify_code,
              "password": password,
              "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "json",
            success: function(data, status){
              if(data === "success"){
                window.location = "/login"
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