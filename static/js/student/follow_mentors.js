/**
 * Created by wushengyu on 15/8/20.
 */
$(document).ready(function(){
  $('#user-position').text("关注导师");
});
function cancelFollow(teacherId){
  $.ajax({
        url: "/user/cancel_follow?mentor_id=" + teacherId,
        type: "get",
        dataType: "json",
        success: function(data, status){
          if(data !== "failed"){
            $('#mentor' + data).remove();
          } else{
            Notify(data);
          }
        }
      }
  )
}

function toMentorDetail(id){
  window.location = "/mentor_detail?mentor_id=" + id;
}