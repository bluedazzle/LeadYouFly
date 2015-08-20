/**
 * Created by wushengyu on 15/8/18.
 */
function toConfirmOrder(courseId){
  console.log("click");
  window.location = "/confirm_order?course_id=" + courseId;
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