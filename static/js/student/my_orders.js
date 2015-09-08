/**
 * Created by wushengyu on 15/8/20.
 */
$(document).ready(function(){
  $('#user-position').text("我的订单")
});

function viewContact(phone, yy, qq){
  $('#mentor-contact').modal('show');
  $('#yy').text(yy);
  $('#phone').text(phone);
  $('#qq').text(qq);
}

function cancelOrder(orderId){
  $.ajax({
    url: '/user/cancel_order',
    type: 'post',
    data: {
      'order_id': orderId,
      'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
    },
    dataType: 'json',
    success: function(data){
      if(data === 'success'){
        location.reload()
      } else{
        Notify("操作失败");
      }
    }
  })
}

function toPay(orderId){
  $('#payModal').modal({backdrop: 'static', keyboard: false});
  $.ajax({
    url: '/user/repay_order/',
    type: 'post',
    data: {
      'order_id': orderId,
      'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
    },
    dataType: 'json',
    success: function(data){
      window.open(data);
    }
  })
}