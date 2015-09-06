/**
 * Created by wushengyu on 15/8/20.
 */
$('.star1').click(function(){
  for (var i = 1; i <= 5; i++){
    if(i === 1){
      $('.star' + String(i)).removeClass('glyphicon-star-empty').addClass('glyphicon-star');
    } else{
      $('.star' + String(i)).removeClass('glyphicon-star').addClass('glyphicon-star-empty');
    }
  }
});

$('.star2').click(function(){
  for (var i = 1; i <= 5; i++){
    if(i <= 2){
      $('.star' + String(i)).removeClass('glyphicon-star-empty').addClass('glyphicon-star');
    } else{
      $('.star' + String(i)).removeClass('glyphicon-star').addClass('glyphicon-star-empty');
    }
  }
});

$('.star3').click(function(){
  for (var i = 1; i <= 5; i++){
    if(i <= 3){
      $('.star' + String(i)).removeClass('glyphicon-star-empty').addClass('glyphicon-star');
    } else{
      $('.star' + String(i)).removeClass('glyphicon-star').addClass('glyphicon-star-empty');
    }
  }
});

$('.star4').click(function(){
  for (var i = 1; i <= 5; i++){
    if(i <= 4){
      $('.star' + String(i)).removeClass('glyphicon-star-empty').addClass('glyphicon-star');
    } else{
      $('.star' + String(i)).removeClass('glyphicon-star').addClass('glyphicon-star-empty');
    }
  }
});

$('.star5').click(function(){
  for (var i = 1; i <= 5; i++){
    $('.star' + String(i)).removeClass('glyphicon-star-empty').addClass('glyphicon-star');
  }
});

function submitAppraise(orderId){
  var stars = $('.star-list .glyphicon-star').size();
  var appraiseContent = $('#appraise_content').val();
  if(stars === 0) {
    Notify("请对课程评分");
    return false;
  }
  if(!appraiseContent) {
    Notify("请填写评价内容");
    return false;
  }
  $.ajax({
        url: "/user/appraise_order",
        type: "post",
        data: {
          "order_id": orderId,
          "stars": parseInt(stars),
          "content": appraiseContent,
          "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
        },
        dataType: "json",
        success: function(data, status){
          if(data === "success"){
            window.location = "/user/my_orders"
          } else{
            Notify(data);
          }
        }
      }
  )
}