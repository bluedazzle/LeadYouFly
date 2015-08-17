var isUpdateCourse = false;
function addCourse (){
  $('#course_info').fadeIn();
  isUpdateCourse = false;
  $('#course_name').val('');
  $('#course_price').val('');
  $('#course_content').val('');

}

function updateCourse (id, name, price, info){
  $('#course_info').fadeIn();
  $('#course_id').val(id);
  isUpdateCourse = true;
  $('#course_name').val(name);
  $('#course_price').val(parseInt(price));
  $('#course_content').val(info);
}
$(document).ready(function(){
  $('#manage_courses').addClass('list-group-item-active');
  $('#submit_course').click(function(){
    var course_name = $('#course_name').val();
    var course_price = $('#course_price').val();
    var course_info = $('#course_content').val();
    if (course_name && course_info && course_price){
      var postData = {course_name: course_name,
                      course_price: course_price,
                      course_info: course_info,
                      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()};
      if(isUpdateCourse){
        postData.id = $('#course_id').val()
      }
      $.ajax({
            url: "/teacher/manage_courses",
            type: "post",
            data: postData,
            dataType: "json",
            success: function(data, status){
              if(data === "success"){
                window.location = "/teacher/manage_courses"
              } else{
                Notify(data);
              }
            }
          }
      )
    }
    else{
      Notify("请填写正确的信息");
    }
  });
});
