/**
 * Created by wushengyu on 15/9/6.
 */
$(document).ready(function(){
  function pollOrder(){
    $.ajax({
          url: "/teacher/poll_orders",
          type: "get",
          data: '',
          dataType: "json",
          success: function(data, status){
            var audio = document.getElementById('notice_music');
            if(data === "success"){
              audio.play();
            }
            else{
              audio.pause();
            }
          }
        }
    )
  }
  pollOrder();

  setInterval(pollOrder, 10000);
});