function Notify(msg){
  $('#noticeModal').modal('show');
  $('#notice-message').text(msg);
  setTimeout(closeNoticeModal, 1500);
}

function closeNoticeModal(){
  $('#noticeModal').modal('hide')
}

function changeMentorStatus(status){
  $.ajax({
    url: '/teacher/change_status?status=' + status,
    type: 'get',
    dataType: 'json',
    success: function(data){
      if(data === 'success'){
        if(status == 1) $('#mentor-status').text("可立即授课");
        else $('#mentor-status').text("休息中");
      } else{
        Notify("您现在暂时无法更改状态");
      }
    }
  })
}
