$(document).ready(function(){
  var boxList = $('.host-teacher-box');
  boxList.each(function(){
    var width = $(this).width();
    $(this).height((0.484 * width).toString());
  });
});

function recommendTeacher(id){
 window.open('/mentor_detail?mentor_id=' + id);
}