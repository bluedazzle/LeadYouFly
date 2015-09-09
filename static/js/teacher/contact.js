$(document).ready(function(){
  $('#teacher_contact').addClass('list-group-item-active');
  $('#submit_contact').click(function(){
    var qq = $('#qq').val();
    var yy = '';
    var phone = $('#phone').val();
    if (qq && phone && phone.length == 11){
      $.ajax({
            url: "/teacher/contact",
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
                window.location = "/teacher/contact"
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