$(document).ready(function(){
  $('#teacher_order_accept').addClass('list-group-item-active');
});

function acceptOrder(orderId){
  $.ajax({
        url: "/teacher/order_accept",
        type: "post",
        data: {
          "orderId": orderId,
          "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
        },
        dataType: "json",
        success: function(data, status){
          if(data === "success"){
            window.location = "/teacher/order_accept"
          } else{
            Notify(data);
          }
        }
      }
  )
}
