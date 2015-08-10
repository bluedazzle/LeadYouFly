/**
 * Created by wushengyu on 15/8/8.
 */
$(document).ready(function(){
  $('#complete_mes_submit').click(function(){
    var qq = $('#qq').val();
    var yy = $('#yy').val();
    var phone = $('#phone').val();
    if (qq && yy && phone && phone.length == 11){
      $.ajax({
            url: "/user/complete_mes",
            type: "post",
            data: {
              "qq": qq,
              "yy": yy,
              "phone": phone,
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