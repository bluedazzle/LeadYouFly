$(document).ready(function(){
  $('#teacher_order_accept').addClass('list-group-item-active');
});

function acceptOrder(orderId){
  $.ajax({
        url: "/teacher/order_accept",
        type: "post",
        data: {
          "order_id": orderId,
          "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
        },
        dataType: "json",
        success: function(data, status){
          if(data === "success"){
            $('#option' + orderId + " button").remove();
            var new_button = "<button class='btn btn-default btn-hg disabled' style='font-size: 18px;'>已接单</button>";
            $('#option' + orderId).append(new_button);
          } else{
            Notify(data);
          }
        }
      }
  )
}
