/**
 * Created by wushengyu on 15/8/11.
 */
$(document).ready(function(){
  $('#user-position').text("消息中心");
  $('body').css('background', 'url(/img/mback.jpg)');
  $('.time-line ul li:odd').addClass('a');
  $('.time-line ul li:even').addClass('b');
  $('.in').each(function(){
    var height = $(this).parent().height();
    $(this).css('height', height+"px");
  });
  $('.b').each(function(){
    var height = $(this).next().height();
    $(this).css('margin-bottom', height+"px");
  });
  $('.a').each(function(){
    var height = $(this).prev().height();
    $(this).css('margin-top', height+"px");
  })
});