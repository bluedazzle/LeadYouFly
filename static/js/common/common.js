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


$(function(){
  var paginationList = $('.pagination .pagination-page');
  var n = paginationList.length;
  var c = paginationList.index($('.pagination .active'));
  var i, y;
  var setp1=c;
  var setp2=n-c; //后余
  if(n>11){
    if(c>5&&c<n-6){
      for (i=3;i<c-3;i++){
        paginationList.eq(i).hide();
      }
      paginationList.eq(2).text('...');
      for (i=c+5; i<n-2; i++){
        paginationList.eq(i).hide();
      }
      paginationList.eq(c+4).text('...')
    } else if(c<=5){
      for (i=9; i<n-3; i++){
        paginationList.eq(i).hide();
      }
      paginationList.eq(i).text('...');
    } else {
      for (i=3; i<n-9; i++){
        paginationList.eq(i).hide();
      }
      paginationList.eq(2).text('...');
    }
  }
});