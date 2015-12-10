/**
 * Created by wushengyu on 15/8/18.
 */

$(document).ready(function(){
  var i = 0;
  $('.view-more').show();
  $('.detail-course-box').each(function(){
    if(i < 2){
      $(this).show();
    }
    i++
  })
});
function toConfirmOrder(courseId, mentor_status){
  if (mentor_status === 3){
    Notify("教练休息中，无法下单");
    return false
  }
    var wechatInfo = navigator.userAgent.match(/MicroMessenger\/([\d\.]+)/i);
    if (wechatInfo) {
        window.location = "/confirm_order?wechat=1&course_id=" + courseId;}
    else{
        window.location = "/confirm_order?wechat=0&course_id=" + courseId;
    }
}

function followMentor(teacherId){
  $.ajax({
        url: "/user/follow_mentor?mentor_id=" + teacherId,
        type: "get",
        dataType: "json",
        success: function(data, status){
          if(data !== "failed"){
            $('#followMentor').find('button').remove();
            $('#followMentor').append("<button class='btn btn-warning' onclick='cancelFollow("+ data +")'>取消关注</button>");
          } else{
            Notify(data);
          }
        }
      }
  )
}

function cancelFollow(teacherId){
  $.ajax({
        url: "/user/cancel_follow?mentor_id=" + teacherId,
        type: "get",
        dataType: "json",
        success: function(data, status){
          if(data !== "failed"){
            $('#followMentor').find('button').remove();
            $('#followMentor').append("<button class='btn btn-warning' onclick='followMentor("+ data +")'>关注</button>");
          } else{
            Notify(data);
          }
        }
      }
  )
}

function viewAllCourses(){
  $('.detail-course-box').fadeIn();
  $('.view-more').hide();
}