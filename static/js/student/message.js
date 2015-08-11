/**
 * Created by wushengyu on 15/8/11.
 */
$(document).ready(function(){
  var nav_height = $('#header').height();
  var footer_height = $('#footer').height();
  var body_height = $('body').height();
  console.log(nav_height);
  console.log(footer_height);
  console.log(body_height);
  $('#page').height(body_height-nav_height-footer_height);
});